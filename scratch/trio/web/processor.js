class TrioProcessor extends AudioWorkletProcessor {

	constructor(options) {
		this.port.onmessage(event) => this.onmessage(event.data)
	}

	process(inputs, outputs, parameters) {

	}

	onmessage(event) {

	}

}

registerProcessor('trio', TrioProcessor)
