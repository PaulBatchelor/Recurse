/*
 * Copyright (c) 2015 Andrew Kelley
 *
 * This file is part of libsoundio, which is MIT licensed.
 * See http://opensource.org/licenses/MIT
 */

#include <soundio/soundio.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#include <inttypes.h>
#include <unistd.h>
#include <linux/input.h>
#include <libevdev/libevdev.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>

typedef struct {
    struct VoxData *vd;
} AudioData;

float testfunction(void);
struct VoxData * newdsp(uint32_t sr);

float testgetter(struct VoxData *vd);
float vox_tick(struct VoxData *vd);
void vox_poll(struct VoxData *vd);
void vox_free(struct VoxData *vd);
void vox_pitch(struct VoxData *vd, float pitch);
void vox_gate(struct VoxData *vd, float gate);
uint8_t vox_running(struct VoxData *vd);

static int usage(char *exe) {
    fprintf(stderr, "Usage: %s [options]\n"
            "Options:\n"
            "  [--backend dummy|alsa|pulseaudio|jack|coreaudio|wasapi]\n"
            "  [--device id]\n"
            "  [--raw]\n"
            "  [--name stream_name]\n"
            "  [--latency seconds]\n"
            "  [--sample-rate hz]\n"
            , exe);
    return 1;
}

static void write_sample_s16ne(char *ptr, double sample) {
    int16_t *buf = (int16_t *)ptr;
    double range = (double)INT16_MAX - (double)INT16_MIN;
    double val = sample * range / 2.0;
    *buf = val;
}

static void write_sample_s32ne(char *ptr, double sample) {
    int32_t *buf = (int32_t *)ptr;
    double range = (double)INT32_MAX - (double)INT32_MIN;
    double val = sample * range / 2.0;
    *buf = val;
}

static void write_sample_float32ne(char *ptr, double sample) {
    float *buf = (float *)ptr;
    *buf = sample;
}

static void write_sample_float64ne(char *ptr, double sample) {
    double *buf = (double *)ptr;
    *buf = sample;
}

static void (*write_sample)(char *ptr, double sample);
static double seconds_offset = 0.0;
static volatile bool want_pause = false;

static void write_callback(struct SoundIoOutStream *outstream, int frame_count_min, int frame_count_max) {
    double float_sample_rate = outstream->sample_rate;
    double seconds_per_frame = 1.0 / float_sample_rate;
    struct SoundIoChannelArea *areas;
    int err;

    int frames_left = frame_count_max;
    AudioData *ad;

    ad = (AudioData *)outstream->userdata;

    for (;;) {
        int frame_count = frames_left;
        if ((err = soundio_outstream_begin_write(outstream, &areas, &frame_count))) {
            fprintf(stderr, "unrecoverable stream error: %s\n", soundio_strerror(err));
            exit(1);
        }

        if (!frame_count)
            break;

        const struct SoundIoChannelLayout *layout = &outstream->layout;

        for (int frame = 0; frame < frame_count; frame += 1) {
            double sample = vox_tick(ad->vd);
            for (int channel = 0; channel < layout->channel_count; channel += 1) {
                write_sample(areas[channel].ptr, sample);
                areas[channel].ptr += areas[channel].step;
            }
        }
        seconds_offset = fmod(seconds_offset + seconds_per_frame * frame_count, 1.0);

        if ((err = soundio_outstream_end_write(outstream))) {
            if (err == SoundIoErrorUnderflow)
                return;
            fprintf(stderr, "unrecoverable stream error: %s\n", soundio_strerror(err));
            exit(1);
        }

        frames_left -= frame_count;
        if (frames_left <= 0)
            break;
    }

    soundio_outstream_pause(outstream, want_pause);
}

static void underflow_callback(struct SoundIoOutStream *outstream) {
    static int count = 0;
    fprintf(stderr, "underflow %d\n", count++);
}

void setup_audio_data(AudioData *ad, uint32_t sr)
{
    ad->vd = newdsp(sr);
}

int main(int argc, char **argv) {
    char *exe = argv[0];
    enum SoundIoBackend backend = SoundIoBackendNone;
    char *device_id = NULL;
    bool raw = false;
    char *stream_name = NULL;
    double latency = 0.0;
    int sample_rate = 0;
    AudioData *ad;

    // explicitely request 44.kHz. On OSX, I think the
    // sample rate suddenly changes to 48kHz, which
    // caused my DSP to be pitched wrong
    sample_rate = 44100;

    for (int i = 1; i < argc; i += 1) {
        char *arg = argv[i];
        if (arg[0] == '-' && arg[1] == '-') {
            if (strcmp(arg, "--raw") == 0) {
                raw = true;
            } else {
                i += 1;
                if (i >= argc) {
                    return usage(exe);
                } else if (strcmp(arg, "--backend") == 0) {
                    if (strcmp(argv[i], "dummy") == 0) {
                        backend = SoundIoBackendDummy;
                    } else if (strcmp(argv[i], "alsa") == 0) {
                        backend = SoundIoBackendAlsa;
                    } else if (strcmp(argv[i], "pulseaudio") == 0) {
                        backend = SoundIoBackendPulseAudio;
                    } else if (strcmp(argv[i], "jack") == 0) {
                        backend = SoundIoBackendJack;
                    } else if (strcmp(argv[i], "coreaudio") == 0) {
                        backend = SoundIoBackendCoreAudio;
                    } else if (strcmp(argv[i], "wasapi") == 0) {
                        backend = SoundIoBackendWasapi;
                    } else {
                        fprintf(stderr, "Invalid backend: %s\n", argv[i]);
                        return 1;
                    }
                } else if (strcmp(arg, "--device") == 0) {
                    device_id = argv[i];
                } else if (strcmp(arg, "--name") == 0) {
                    stream_name = argv[i];
                } else if (strcmp(arg, "--latency") == 0) {
                    latency = atof(argv[i]);
                } else if (strcmp(arg, "--sample-rate") == 0) {
                    sample_rate = atoi(argv[i]);
                } else {
                    return usage(exe);
                }
            }
        } else {
            return usage(exe);
        }
    }

    struct SoundIo *soundio = soundio_create();
    if (!soundio) {
        fprintf(stderr, "out of memory\n");
        return 1;
    }

    int err = (backend == SoundIoBackendNone) ?
        soundio_connect(soundio) : soundio_connect_backend(soundio, backend);

    if (err) {
        fprintf(stderr, "Unable to connect to backend: %s\n", soundio_strerror(err));
        return 1;
    }

    fprintf(stderr, "Backend: %s\n", soundio_backend_name(soundio->current_backend));

    soundio_flush_events(soundio);

    int selected_device_index = -1;
    if (device_id) {
        int device_count = soundio_output_device_count(soundio);
        for (int i = 0; i < device_count; i += 1) {
            struct SoundIoDevice *device = soundio_get_output_device(soundio, i);
            bool select_this_one = strcmp(device->id, device_id) == 0 && device->is_raw == raw;
            soundio_device_unref(device);
            if (select_this_one) {
                selected_device_index = i;
                break;
            }
        }
    } else {
        selected_device_index = soundio_default_output_device_index(soundio);
    }

    if (selected_device_index < 0) {
        fprintf(stderr, "Output device not found\n");
        return 1;
    }

    struct SoundIoDevice *device = soundio_get_output_device(soundio, selected_device_index);
    if (!device) {
        fprintf(stderr, "out of memory\n");
        return 1;
    }

    fprintf(stderr, "Output device: %s\n", device->name);

    if (device->probe_error) {
        fprintf(stderr, "Cannot probe device: %s\n", soundio_strerror(device->probe_error));
        return 1;
    }

    struct SoundIoOutStream *outstream = soundio_outstream_create(device);
    if (!outstream) {
        fprintf(stderr, "out of memory\n");
        return 1;
    }

    ad = malloc(sizeof(AudioData));

    outstream->userdata = ad;
    outstream->write_callback = write_callback;
    outstream->underflow_callback = underflow_callback;
    outstream->name = stream_name;
    outstream->software_latency = latency;
    outstream->sample_rate = sample_rate;

    if (soundio_device_supports_format(device, SoundIoFormatFloat32NE)) {
        outstream->format = SoundIoFormatFloat32NE;
        write_sample = write_sample_float32ne;
    } else if (soundio_device_supports_format(device, SoundIoFormatFloat64NE)) {
        outstream->format = SoundIoFormatFloat64NE;
        write_sample = write_sample_float64ne;
    } else if (soundio_device_supports_format(device, SoundIoFormatS32NE)) {
        outstream->format = SoundIoFormatS32NE;
        write_sample = write_sample_s32ne;
    } else if (soundio_device_supports_format(device, SoundIoFormatS16NE)) {
        outstream->format = SoundIoFormatS16NE;
        write_sample = write_sample_s16ne;
    } else {
        fprintf(stderr, "No suitable device format available.\n");
        return 1;
    }

    setup_audio_data(ad, device->sample_rate_current);

    if ((err = soundio_outstream_open(outstream))) {
        fprintf(stderr, "unable to open device: %s", soundio_strerror(err));
        return 1;
    }

    fprintf(stderr, "Software latency: %f\n", outstream->software_latency);
    fprintf(stderr,
            "'p\\n' - pause\n"
            "'u\\n' - unpause\n"
            "'P\\n' - pause from within callback\n"
            "'c\\n' - clear buffer\n"
            "'q\\n' - quit\n");

    if (outstream->layout_error)
        fprintf(stderr, "unable to set channel layout: %s\n", soundio_strerror(outstream->layout_error));

    if ((err = soundio_outstream_start(outstream))) {
        fprintf(stderr, "unable to start device: %s\n", soundio_strerror(err));
        return 1;
    }

    struct libevdev *dev = NULL;
    int fd;
    int rc = 1;

    const char *devpath ="/dev/input/by-id/usb-Wacom_Co._Ltd._Intuos_PTM-event-mouse";
    fd = open(devpath, O_RDONLY|O_NONBLOCK);
    rc = libevdev_new_from_fd(fd, &dev);
    if (rc < 0) {
        //fprintf(stderr, "Failed to init libevdev (%s)\n", strerror(-rc));
        fprintf(stderr, "error: %d\n", rc);
        exit(1);
    }

    vox_gate(ad->vd, 0);
    int touching = 0;
    while(vox_running(ad->vd)) {
        soundio_flush_events(soundio);

        struct input_event ev;

        rc = libevdev_next_event(dev, LIBEVDEV_READ_FLAG_NORMAL, &ev);

        if (rc == 0) {
            int on_touch;

            on_touch =
                ev.type == EV_KEY &&
                ev.code == BTN_TOUCH;

            if (on_touch) {

                if (ev.value == 1) {
                    touching = 1;
                    vox_gate(ad->vd, 1);
                } else {
                    touching = 0;
                    vox_gate(ad->vd, 0);
                }
                printf("touching is now %d\n", touching);
            }

            int please_print = ev.type == EV_ABS && (ev.code == ABS_X);
            if (please_print && touching == 1) {

                if (ev.code == ABS_X) {
                    float x_axis;
                    float pitch;

                    x_axis = ev.value / 21600.0;
                    pitch = 48.0 + (12.0 * 3) * x_axis;

                    vox_pitch(ad->vd, pitch);

                } else if (ev.code == ABS_PRESSURE) {
                    // float gate;

                    // gate = ev.value > 0;
                    // vox_gate(ad->vd, gate);


                }
            }
        }

        //vox_poll(ad->vd);
        // int c = getc(stdin);
        // if (c == 'p') {
        //     fprintf(stderr, "pausing result: %s\n",
        //             soundio_strerror(soundio_outstream_pause(outstream, true)));
        // } else if (c == 'P') {
        //     want_pause = true;
        // } else if (c == 'u') {
        //     want_pause = false;
        //     fprintf(stderr, "unpausing result: %s\n",
        //             soundio_strerror(soundio_outstream_pause(outstream, false)));
        // } else if (c == 'c') {
        //     fprintf(stderr, "clear buffer result: %s\n",
        //             soundio_strerror(soundio_outstream_clear_buffer(outstream)));
        // } else if (c == 'q') {
        //     break;
        // } else if (c == '\r' || c == '\n') {
        //     // ignore
        // } else {
        //     fprintf(stderr, "Unrecognized command: %c\n", c);
        // }
    }

    soundio_outstream_destroy(outstream);
    soundio_device_unref(device);
    soundio_destroy(soundio);

    vox_free(ad->vd);
    free(ad);
    return 0;
}
