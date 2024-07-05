class ChatterSynth extends AudioWorkletProcessor {
    constructor(options) {
        super(options)
        const wasmBytes = options.processorOptions.wasmBytes;
        const mod = new WebAssembly.Module(wasmBytes);
        this.wasm = new WebAssembly.Instance(mod, {});
        //this.gpath = this.wasm.exports.genseq();
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
        if (event.type === "poke") {
            this.wasm.exports.poke(this.dsp);
        } else if (event.type === "mouthopen-get") {
            let m = this.wasm.exports.mouth_open(this.dsp);
            this.port.postMessage({type: "mouthopen-rsp", data:m});
        } else if (event.type === "mouthstate-get") {
            let cur = this.wasm.exports.mouth_curshape(this.dsp);
            let nxt = this.wasm.exports.mouth_nxtshape(this.dsp);
            let pos = this.wasm.exports.mouth_pos(this.dsp);
            this.port.postMessage({type: "mouthstate-rsp", data:[cur, nxt, pos]});
        }
    }

}

registerProcessor('chatter', ChatterSynth);
