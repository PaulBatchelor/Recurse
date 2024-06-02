mkdir -p singer_test
rsync -rvt dsp.wasm index.html index.js singer.js singer_test
rsync -rvt singer_test paul@pbat.ch:paulbatchelor.github.io/recurse/demos
