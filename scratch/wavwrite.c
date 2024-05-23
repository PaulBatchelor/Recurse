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
    /* one chunk for format, one chunk for PCM data */
    cksize = 4 + 2;
    write_str(wav, "RIFF", 4);
    write_uint32(wav, cksize);
    write_str(wav, "WAVE", 4);
}

void write_fmt_chunk(FILE *wav)
{
    uint32_t cksize;

    write_str(wav, "fmt ", 4);

    cksize = 0;
    /* format code: WAVE_FORMAT_PCM (0x0001) */
    write_uint16(wav, 0x0001);
    cksize += 2;

    /* nchannels: 1 (always mono) */
    write_uint16(wav, 0x0001);
    cksize += 2;

    /* sampling rate: 44.kHz hardcoded for now */
    write_uint32(wav, 44100);
    cksize += 4;

    /* average bytes per second: huh? */
    /* constant bitrate 32-bit float at 44.1kHz */
    write_uint32(wav, 44100 / 4);
    cksize += 4;

    /* TODO: bits-per-second */
    /* TODO: extension size */
    /* TODO: valid bits per sample */
    /* TODO: speaker position mask */
    /* TODO: subformat */

    printf("chunk size: %d\n", cksize);
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

    fclose(wav);
    fclose(fp);
    return 0;
}
