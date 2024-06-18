default: voxboxOSC

OBJ=main.o

CFLAGS=-Wall -pedantic -O3
LDFLAGS=-L$(DSPLIBPATH)

CFLAGS += -I/opt/homebrew/include
LDFLAGS += -L/opt/homebrew/lib

LIBS=-lsoundio -lvoxdsp

DSPLIBPATH=voxdsp/target/release
DSPLIB=$(DSPLIBPATH)/libvoxdsp.a


voxboxOSC: $(OBJ) $(DSPLIB)
	$(CC) $(CFLAGS) $(OBJ) -o $@ $(LDFLAGS) $(LIBS)

RUST_FILES=voxdsp/src/lib.rs

$(DSPLIB): $(RUST_FILES)
	cd voxdsp; cargo build --release

clean:
	$(RM) $(OBJ) voxboxOSC
	cd voxdsp; cargo clean
