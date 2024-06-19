const audioContext = new AudioContext();
let SingerNode = null;

buttonList = [];
lastSelected = -1;

const Chords = [
        [0, 7, 0, 4],
        [-2, 7, 0, 2],
        [0, 7, 4, 5],
        [0, 4, 5, 7],
        [-4, 3, 0, 8],
        [-5, 5, 2, 10],
        [-12, 0, 4, 12],
        [-12, 14, 4, 12],
        [-12, 12, 4, 12],
        [-12, 16, 2, 12],
        [-12, 16, 5, 12],
        [-12, 14, 5, 12],
]

class VocalChordsWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
        this.base = 63;
        this.setChordWithBase(Chords[0], -this.base);
        //this.setChord(Chords[1]);
    }

    setChordWithBase(chord, base) {
        console.log("base: " + base);
        let transposed_chord = [0, 0, 0, 0];
        for (let i = 0; i < 4; i++) {
            transposed_chord[i] = chord[i];
            transposed_chord[i] += Math.abs(base);
            transposed_chord[i] *= Math.sign(base);
            console.log("Chord: " + transposed_chord[i]);
        }

        this.port.postMessage({type: "chord", data: transposed_chord});
    }

    setChord(chord) {
        this.setChordWithBase(chord, this.base);
    }

}

function addHorizSlider(name, minVal, maxVal, defaultVal, step, updateValue) {
    const control = document.createElement('p')
    control.textContent = capitalizeFirstLetter(name) + ': ';
    const slider = document.createElement('input');
    const output = document.createElement('output');

    slider.type = "range";
    slider.min = minVal;
    slider.max = maxVal;
    slider.id = name;
    slider.step = step;
    slider.value = defaultVal;

    output.id = name + '-value';
    output.textContent = slider.value;

    slider.addEventListener("input", (event) => {
        output.textContent = event.target.value;
        updateValue(event.target.value);
    });

    control.appendChild(slider);
    control.appendChild(output);

    return control;
}

// https://stackoverflow.com/questions/1026069/how-do-i-make-the-first-letter-of-a-string-uppercase-in-javascript
function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function add_controls() {
    const controls = document.getElementById('controls');
    let grid = document.createElement('div');
    grid.id = 'container';
    for (let i = 0; i < Chords.length; i++) {
        let rect = document.createElement('div');
        let btn = document.createElement('button');
        buttonList[i] = btn;

        btn.textContent = i;
        btn.className = 'chordbutton';
        btn.addEventListener('click', () => {
            if (SingerNode !== null) {
                SingerNode.setChord(Chords[i]);
                buttonList[i].className = 'chordbutton-selected';
                if (lastSelected >= 0) {
                    buttonList[lastSelected].className = 'chordbutton';
                }
                lastSelected = i;

            }
        });
        rect.appendChild(btn);
        grid.appendChild(rect);
    }
    controls.appendChild(grid);
}

const startAudio = async (context) => {
    try {
        await context.audioWorklet.addModule('vocal_chords.js');
    } catch(e) {
        throw new Error(`noise generator error: ${e.message}`);
    }

    const wasmFile = await fetch('dsp.wasm');
    const wasmBuffer = await wasmFile.arrayBuffer();

    const options = {
        wasmBytes: wasmBuffer
    };
    const Singer = new
        VocalChordsWorkletNode(context, 'singer', {
            processorOptions: options
        });

    Singer.connect(context.destination);
    SingerNode = Singer;
};

audioStarted = false
audioPaused = true

window.addEventListener('load', async () => {
    const buttonBegin = document.getElementById('button-begin');
    console.log(audioContext.state);
    buttonBegin.addEventListener('click', async () => {
        if (audioStarted === false) {
            audioStarted = true;
            await startAudio(audioContext);
            audioContext.resume();
            buttonBegin.textContent = 'Playing...';
            audioPaused = false;
        } else {
            if (audioPaused) {
                buttonBegin.textContent = 'Playing...';
                audioContext.resume();
                audioPaused = false;
            } else {
                buttonBegin.textContent = 'Stopped';
                audioPaused = true;
                audioContext.suspend();
            }
        }
    }, false);

    add_controls();
});
