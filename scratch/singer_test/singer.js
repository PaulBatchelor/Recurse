class SingerSynth extends AudioWorkletProcessor {
    constructor(options) {
        super(options)
        const wasmBytes = options.processorOptions.wasmBytes;
        const mod = new WebAssembly.Module(wasmBytes);
        this.wasm = new WebAssembly.Instance(mod, {});
        this.dsp = this.wasm.exports.newdsp(sampleRate);
        this.outptr = this.wasm.exports.alloc(128);
        this.outbuf = new Float32Array(this.wasm.exports.memory.buffer,
                this.outptr,
                128);

        this.port.onmessage = (event) => this.onmessage(event.data);
    }

    process(inputs, outputs, parameters) {
        const output = outputs[0];
        this.wasm.exports.process(this.dsp, this.outptr, 128);
        for (let channel = 0; channel < output.length; ++channel) {
            const outputChannel = output[channel];
            for (let i = 0; i < outputChannel.length; ++i) {
                outputChannel[i] = this.outbuf[i];
            }
        }

        return true;
    }

    onmessage(event) {
        if (event.type === "pitch") {
            this.wasm.exports.set_pitch(this.dsp, event.data);
        } else if (event.type === "aspiration") {
            this.wasm.exports.set_aspiration(this.dsp, event.data);
        } else if (event.type === "noise_floor") {
            this.wasm.exports.set_noise_floor(this.dsp, event.data);
        } else if (event.type === "shape") {
            this.wasm.exports.set_shape(this.dsp, event.data);
        } else if (event.type === "velum") {
            this.wasm.exports.set_velum(this.dsp, event.data);
        } else if (event.type === "regset") {
            this.wasm.exports.set_region(this.dsp, event.region, event.value);
        }
    }

}

registerProcessor('singer', SingerSynth);
