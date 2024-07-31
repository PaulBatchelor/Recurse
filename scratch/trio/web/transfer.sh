DEMO_NAME=trio
mkdir -p $DEMO_NAME
rsync -rvt dsp.wasm index.html style.css main.js audio.js processor.js  $DEMO_NAME
rsync -rvt $DEMO_NAME paul@pbat.ch:paulbatchelor.github.io/recurse/demos
