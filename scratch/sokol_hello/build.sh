cc  clear-sapp.c \
    sokol.m \
    -o clear-sapp \
    -I. \
    -DSOKOL_METAL \
    -fobjc-arc \
    -framework Metal \
    -framework Cocoa -framework MetalKit -framework Quartz \
    -framework AudioToolBox
