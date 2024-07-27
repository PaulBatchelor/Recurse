NINJAFILE=build.ninja

>$NINJAFILE

cat >>$NINJAFILE <<EOM
stretcher_util =~/proj/stretcher/stretcher
input_wav = wendy.wav

rule trimmer
    command = sox \$input_wav -c 1 \$out trim \$start =\$end

rule trimmer2
    command = sox \$in -c 1 \$out trim \$start =\$end

rule paulstretch
    command = \$stretcher_util \$windowsize \$stretch \$in \$out && sox \$out tmp.wav norm -1 && mv tmp.wav \$out

rule mix
    command = sox -m \$in \$out

rule rustc
    command = rustc \$in

rule pulse
    command = ./pulse \$in \$out

rule raw2wav
    command = sox -t raw -c 1 -r 44100 -e floating-point -b 32 \$in \$out

rule repeat
    command = sox \$in \$out repeat \$nreps

rule lil
    command = mnolth lil \$in

rule lua
    command = mnolth lua \$in
EOM

LIL="mnolth lil"

$LIL trimmer.lil >> $NINJAFILE
$LIL finetrim.lil >> $NINJAFILE
$LIL ps.lil >> $NINJAFILE
$LIL mix.lil >> $NINJAFILE

cat >> $NINJAFILE <<EOM
build pulse: rustc pulse.rs
build pulse.bin: pulse pulse.txt || pulse
build pulse.wav: raw2wav pulse.bin
build pulsereps.wav: repeat pulse.wav
    nreps = 8
build pulsetest.wav: lil pulsetest.lil | pulsereps.wav finetrim_subgroove.wav
build bassgroove.wav: lil bassgroove.lil | pulsereps.wav finetrim_subgroove.wav
build clicker.wav: lua clicker.lua| pulsereps.wav finetrim_click.wav snare.wav
build snare.wav: lua snare.lua| finetrim_noise.wav
EOM
