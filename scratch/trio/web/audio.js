class TrioWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
    }

    move(x, y) {
        this.port.postMessage({type: "move", x: x, y: y});
    }


    on() {
        this.port.postMessage({type: "on"});
    }

    off() {
        this.port.postMessage({type: "off"});
    }
}

async function startAudio(context) {
    try {
        await context.audioWorklet.addModule('processor.js');
    } catch (e) {
        throw new Error(`Could not load processor: ${e.message}`);
    }

    // TODO load wasm 

    const options = {
        wasmBytes: [],
    }

    let nd = new TrioWorkletNode(context, 'trio', {
        processorOptions: options
    });

    nd.connect(context.destination);

    return nd
}

export { startAudio };
