# VoxBoxOSC
Control VoxBox using OSC.

## Building

To build:

Have rust installed, libsoundio, and a standard Posix
toolchain (Make, gcc/clang, etc)

Make sure the [voxbox repo](github.com/paulbatchelor/voxbox)
is cloned next to this Recurse monorepo.

Run "make" to build

Run "./voxboxOSC" to run

## OSC Messages
OSC messages run on port 8001.

- /quit: gracefully stops the synth
- /vox/gain (f): sets the volume gain, in linear units (0-1)
- /vox/pitch (f): sets the pitch of the using MIDI note numbers
- /vox/tongue (ff): sets tongue shape (each parameter in range 0-1)
- /vox/tsmooth (f): sets smoothing amount of tongue control (0 is off, 0.03 is good for smooth jumps, 1.5 is good for builds, etc)
