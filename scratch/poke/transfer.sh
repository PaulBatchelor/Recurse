DEMO_NAME=poke
mkdir -p $DEMO_NAME
rsync -rvt dsp.wasm index.html sketch.js p5.min.js chatter.js sketch.css $DEMO_NAME
rsync -rvt $DEMO_NAME paul@pbat.ch:paulbatchelor.github.io/recurse/demos
