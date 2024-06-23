build_linux() {
    cc  clear-sapp.c sokol.c \
        -o clear-sapp \
        -I. \
        -DSOKOL_GLCORE \
        -lasound \
        -lm \
        -lGL \
        -lX11 \
        -lXi \
        -lXcursor
}

build_osx() {
    cc  clear-sapp.c \
        sokol.m \
        -o clear-sapp \
        -I. \
        -DSOKOL_METAL \
        -fobjc-arc \
        -framework Metal \
        -framework Cocoa -framework MetalKit -framework Quartz \
        -framework AudioToolBox
}

PLATFORM=$(uname | tr '[:upper:]' '[:lower:]')

if [ $PLATFORM == "linux" ]
then
    build_linux
else
    build_osx
fi
