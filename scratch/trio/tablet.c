#include <stdio.h>
#include <linux/input.h>
#include <math.h>

struct VoxData;
void vox_pitch(struct VoxData *vd, float pitch);
void vox_tongue_shape(struct VoxData *vd, float x, float y);
void vox_gate(struct VoxData *vd, float gate);


float pitches[] = {
    0, 2, 4, 5, 7, 9, 11, 12, 14, 16
};

void handle_tablet_event(struct VoxData *vd,
    struct input_event *ev,
    int *touching) {

    int on_touch;

    on_touch =
        ev->type == EV_KEY &&
        ev->code == BTN_TOUCH;

    if (on_touch) {

        if (ev->value == 1) {
            *touching = 1;
            vox_gate(vd, 1);
        } else {
            *touching = 0;
            vox_gate(vd, 0);
        }
    }

    int please_print = ev->type == EV_ABS;
    if (please_print && *touching == 1) {
        if (ev->code == ABS_X) {
            float x_axis;
            float pitch;
            float base;
            float max_xres;

            base = 60.0;
            max_xres = 32767.0;

            //x_axis = ev.value / 21600.0;
            //x_axis = ev.value / 46024.0;
            x_axis = ev->value / max_xres;
            //pitch = 48.0 + (12.0 * 4) * x_axis;
            pitch = floor(10 * x_axis);
            pitch = base + pitches[(int)pitch];
            //pitch = 24.0 + (12.0 * 2) * x_axis;

            vox_pitch(vd, pitch);

        } else if (ev->code == ABS_Y) {
            float y_axis;
            y_axis = ev->value / 32767.0;
            y_axis = 0.1 + y_axis * 0.8;
            //vox_tongue_shape(vd, 0.1, y_axis);
        } else if (ev->code == ABS_PRESSURE) {
            // float gate;

            // gate = ev.value > 0;
            // vox_gate(ad->vd, gate);


        }
    }
}
