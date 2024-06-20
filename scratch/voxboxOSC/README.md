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

- /vox/pitch (f): sets the pitch of the using MIDI note numbers
- /vox/gain (f): sets the volume gain, in linear units (0-1)
- /quit: gracefully stops the synth
