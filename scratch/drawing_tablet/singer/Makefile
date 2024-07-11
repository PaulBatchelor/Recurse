default: singer_tablet_test

OBJ=main.o tablet.o

CFLAGS=-Wall -pedantic -O3
LDFLAGS=-L$(DSPLIBPATH)

CFLAGS += -I/opt/homebrew/include -g
LDFLAGS += -L/opt/homebrew/lib

CFLAGS += -I/usr/include/libevdev-1.0/
LIBS=-lsoundio -lvoxdsp -levdev

DSPLIBPATH=dsp/target/release
DSPLIB=$(DSPLIBPATH)/libvoxdsp.a


singer_tablet_test: $(OBJ) $(DSPLIB)
	$(CC) $(CFLAGS) $(OBJ) -o $@ $(LDFLAGS) $(LIBS)

RUST_FILES=dsp/src/lib.rs

$(DSPLIB): $(RUST_FILES)
	cd dsp; cargo build --release

clean:
	$(RM) $(OBJ) singer_tablet_test
	cd dsp; cargo clean
