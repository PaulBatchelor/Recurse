class TrioProcessor extends AudioWorkletProcessor {
    constructor(options) {
        super(options);
        this.port.onmessage =
            (event) => this.onmessage(event.data);
    }

    process(inputs, outputs, parameters) {
        // TODO
    }

    onmessage(event) {
        console.log('hello');
        console.log(event.type);

        if (event.type == "move") {
            console.log("processor move", event.x, event.y);
        }
    }
}

registerProcessor('trio', TrioProcessor);
