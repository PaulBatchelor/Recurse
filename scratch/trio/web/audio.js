function startAudio(context) {
	console.log("setting up sound")
}

function setupSynthBindings(sketch, context) {
	sketch.audioContext = context

	sketch.synth_move = (x, y) => {
		console.log("synth move", x, y)
	}
}

export { startAudio }
