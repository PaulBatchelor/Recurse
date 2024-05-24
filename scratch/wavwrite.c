/* bare bones mono wav writer */
/* https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html */

#include <stdio.h>
#include <stdint.h>

void write_uint32(FILE *wav, uint32_t val)
{
    uint32_t *pval;
    pval = &val;
    /* should be little-endian encoding already */
    fwrite(pval, 1, 4, wav);
}

void write_uint16(FILE *wav, uint16_t val)
{
    uint16_t *pval;
    pval = &val;
    /* should be little-endian encoding already */
    fwrite(pval, 1, 2, wav);
}

void write_str(FILE *wav, const char *str, int sz)
{
    fwrite(str, 1, sz, wav);
}

void write_master_chunk(FILE *wav)
{
    uint32_t cksize;

    /* 4 + n, n = 2 */
    /* 4 constant */
    /* cksize = 4;
    /* 16: fmt chunk */
    /* cksize += 16; */
    /* data chunk size */
    /* cksize += 44096 * 2; */

    /* not sure, where these extra 16 bytes come from. */
    /* cksize += 16; */
    write_str(wav, "RIFF", 4);
    write_uint32(wav, 0);
    write_str(wav, "WAVE", 4);
}

void write_fmt_chunk(FILE *wav)
{
    write_str(wav, "fmt ", 4);

    /* chunk size: 16 */
    write_uint32(wav, 0x10);

    /* format code: WAVE_FORMAT_PCM (0x0001) */
    write_uint16(wav, 0x0001);

    /* nchannels: 1 (always mono) */
    write_uint16(wav, 0x0001);

    /* sampling rate: 44.kHz hardcoded for now */
    write_uint32(wav, 44100);

    /* average bytes per second: huh? */
    /* goal: 16-bit at 44.1kHz @ 2 bytes/sample */
    write_uint32(wav, 44100 * 2);

    /* block alignment of waveform data, in bytes. I think this is just 2 bytes? */
    write_uint16(wav, 2);

    /* bits-per-sample */
    write_uint16(wav, 16);
}

void write_data_chunk(FILE *wav)
{
    write_str(wav, "data", 4);
    /* to be written later */
    write_uint32(wav, 0);
}

uint32_t write_data(FILE *wav, FILE *data)
{
    uint32_t nbytes;

    nbytes = 0;
#if 0
    for (i = 0; i < nsamps; i++) {
        /* convert from float to 16-bit signed int */
        int16_t s16;
        float f;

        f = 0;

        fread(&f, 1, 4, data);
        s16 = f * 0x8000;
        nbytes += fwrite(&s16, 1, 2, wav);
    }
#endif

    rewind(data);
    while (!feof(data)) {
        /* convert from float to 16-bit signed int */
        int16_t s16;
        float f;
        int bytes_read;
        f = 0;
        bytes_read = fread(&f, 1, 4, data);
        if (bytes_read< 4) break;
        s16 = f * 0x8000;
        nbytes += fwrite(&s16, 1, 2, wav);
    }

    printf("%d bytes written\n", nbytes);
    return nbytes;
}

void update_chunks(FILE *wav, uint32_t nbytes)
{
    /* update RIFF chunk size */
    fseek(wav, 0x04, SEEK_SET);

    write_uint32(wav, nbytes + 16 + 16 + 4);

    /* update data size */
    fseek(wav, 0x28, SEEK_SET);

    write_uint32(wav, nbytes);
}

int main(int argc, char *argv[])
{
    FILE *fp;
    FILE *wav;
    const char *wav_fname;
    const char *data_fname;

    uint32_t nbytes;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s in.bin out.wav\n", argv[0]);
        return 1;
    }

    data_fname = argv[1];
    wav_fname = argv[2];

    fp = fopen(data_fname, "r");
    wav = fopen(wav_fname, "w");

    write_master_chunk(wav);
    write_fmt_chunk(wav);
    write_data_chunk(wav);
    nbytes = write_data(wav, fp);
    update_chunks(wav, nbytes);

    fclose(wav);
    fclose(fp);
    return 0;
}
