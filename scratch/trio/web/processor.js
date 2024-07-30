class TrioProcessor extends AudioWorkletProcessor {
    constructor(options) {
        super(options);
        const wasmBytes = options.processorOptions.wasmBytes;

        const mod = new WebAssembly.Module(wasmBytes);
        this.wasm = new WebAssembly.Instance(mod, {});

        this.dsp = this.wasm.exports.newdsp(sampleRate);
        this.outptr = this.wasm.exports.alloc(128);
        this.outbuf = new Float32Array(
            this.wasm.exports.memory.buffer,
            this.outptr,
            128
        );
        this.port.onmessage =
            (event) => this.onmessage(event.data);
    }

    process(inputs, outputs, parameters) {
        const output = outputs[0];

        console.log("hello there");
        this.wasm.exports.process(this.dsp, this.outptr, 128);
        for (let c = 0; c < output.length; ++c) {
            const outChan = output[c];
            for (let i = 0; i < outChan.length; ++i) {
                //outChan[i] = this.outbuf[i];
                outChan[i] = Math.random() * 0.1;
            }
        }
    }

    onmessage(event) {
        if (event.type == "move") {
            console.log("processor move", event.x, event.y);
            this.wasm.exports.vox_x_axis(event.x);
            this.wasm.exports.vox_y_axis(event.y);
        } else if (event.type == "off") {
            console.log("proc up");
            this.wasm.exports.vox_gate(0.0);
        } else if (event.type == "on") {
            console.log("proc down 2");
            this.wasm.exports.vox_gate(1.0);
        }
    }
}

registerProcessor('trio', TrioProcessor);
