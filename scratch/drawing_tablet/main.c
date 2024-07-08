#include <stdio.h>
#include <inttypes.h>
#include <unistd.h>
#include <stdlib.h>
#include <linux/input.h>
#include <libevdev/libevdev.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>


int main(int argc, char *argv[])
{
    struct libevdev *dev = NULL;
    int fd;
    int rc = 1;

    fd = open("/dev/input/event16", O_RDONLY|O_NONBLOCK);
    rc = libevdev_new_from_fd(fd, &dev);
    if (rc < 0) {
        //fprintf(stderr, "Failed to init libevdev (%s)\n", strerror(-rc));
        fprintf(stderr, "error: %d\n", rc);
        exit(1);
    }
    printf("Input device name: \"%s\"\n", libevdev_get_name(dev));
    printf("Input device ID: bus %#x vendor %#x product %#x\n",
            libevdev_get_id_bustype(dev),
            libevdev_get_id_vendor(dev),
            libevdev_get_id_product(dev));

    do {
        struct input_event ev;
        rc = libevdev_next_event(dev, LIBEVDEV_READ_FLAG_NORMAL, &ev);
        if (rc == 0)
            if (ev.type== EV_ABS && (ev.code == ABS_X)) {
                printf("Event: %s %s %d (%d %d)\n",
                        libevdev_event_type_get_name(ev.type),
                        libevdev_event_code_get_name(ev.type, ev.code),
                        ev.value, ev.type, ev.code);
            }
    } while (rc == 1 || rc == 0 || rc == -EAGAIN);
    return 0;
}
