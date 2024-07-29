import { sketch } from "./sketch.js";
import { startAudio } from "./audio.js";

const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioContext = new AudioContext()

let canvas = document.getElementById('sketch')

let audioStarted = false

canvas.addEventListener('click', async () => {
	if (!audioStarted) {
		audioStarted = true
		startAudio(audioContext)
	}
})

class TrioGraphics extends p5 {
	constructor(sketch, canvas, audioContext) {
		super(sketch, canvas)
		this.audioContext = audioContext;
		this.pointerDown = false
	}

	pointerMove(x, y) {
		if (audioStarted && this.pointerDown) {
			console.log("synth move", x, y)
		}
	}

	pointerOn() {
		if (audioStarted) {
			this.pointerDown = true
			console.log("synth on");
		}
	}

	pointerOff() {
		if (audioStarted) {
			this.pointerDown = false
			console.log("synth off");
		}
	}
}

new TrioGraphics(sketch, canvas, audioContext)
