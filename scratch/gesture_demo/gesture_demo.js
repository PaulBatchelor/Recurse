class SingerSynth extends AudioWorkletProcessor {
    constructor(options) {
        super(options)
        const wasmBytes = options.processorOptions.wasmBytes;
        const mod = new WebAssembly.Module(wasmBytes);
        this.wasm = new WebAssembly.Instance(mod, {});
        this.gpath = this.wasm.exports.genseq();
        this.dsp = this.wasm.exports.newdsp(sampleRate, this.gpath);
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
        if (event.type === "tempo") {
            this.wasm.exports.set_tempo(this.dsp, event.data);
        }
    }

}

registerProcessor('singer', SingerSynth);
