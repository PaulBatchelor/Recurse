cargo build --target wasm32-unknown-unknown --release
wasm-gc target/wasm32-unknown-unknown/release/singer_test.wasm dsp.wasm
