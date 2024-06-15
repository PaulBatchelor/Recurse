mkdir -p gesture_demo
rsync -rvt dsp.wasm index.html index.js gesture_demo.js style.css gesture_demo
rsync -rvt gesture_demo paul@pbat.ch:paulbatchelor.github.io/recurse/demos
