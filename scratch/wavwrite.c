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
    cksize = 4;
    /* 16: fmt chunk */
    cksize += 16;
    /* data chunk size */
    cksize += 44096 * 2;

    /* not sure, where these extra 16 bytes come from. */
    cksize += 16;
    write_str(wav, "RIFF", 4);
    write_uint32(wav, cksize);
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
    uint32_t sz;

    /* temporary hard-coded size nsamples * 2 bytes/samp */

    sz = 44096 * 2;
    write_str(wav, "data", 4);
    write_uint32(wav, sz);
}

uint32_t get_nsamps(FILE *data)
{
    uint32_t nsamps;
    fseek(data, 0L, SEEK_END);
    nsamps = ftell(data);
    nsamps /= 4; /* 32-bit float: 4 bytes per sample */
    rewind(data);
    return nsamps;
}

void write_data(FILE *wav, FILE *data)
{
    uint32_t nsamps, i;
    uint32_t nbytes;

    nsamps = get_nsamps(data);
    printf("nsamps is now %d\n", nsamps);
    nbytes = 0;

    for (i = 0; i < nsamps; i++) {
        /* convert from float to 16-bit signed int */
        int16_t s16;
        float f;

        f = 0;

        fread(&f, 1, 4, data);
        s16 = f * 0x8000;
        nbytes += fwrite(&s16, 1, 2, wav);
    }

    printf("%d bytes written\n", nbytes);
}

int main(int argc, char *argv[])
{
    FILE *fp;
    FILE *wav;
    uint32_t nsamps;

    fp = fopen("test.bin", "r");
    wav = fopen("test.wav", "w");
    fseek(fp, 0L, SEEK_END);
    nsamps = ftell(fp);
    nsamps /= 4; /* 32-bit float: 4 bytes per sample */
    printf("nsamps: %d\n", nsamps);

    write_master_chunk(wav);
    write_fmt_chunk(wav);
    write_data_chunk(wav);
    write_data(wav, fp);

    fclose(wav);
    fclose(fp);
    return 0;
}
