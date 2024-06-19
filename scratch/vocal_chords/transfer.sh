DEMO_NAME=vocal_chords
mkdir -p $DEMO_NAME
rsync -rvt dsp.wasm index.html index.js vocal_chords.js style.css $DEMO_NAME
rsync -rvt $DEMO_NAME paul@pbat.ch:paulbatchelor.github.io/recurse/demos
