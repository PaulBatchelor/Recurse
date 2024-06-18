default: voxboxOSC

OBJ=main.o

CFLAGS=-Wall -pedantic

LIBS=-lsoundio

voxboxOSC: $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $@ $(LIBS)

clean:
	$(RM) $(OBJ) voxboxOSC
