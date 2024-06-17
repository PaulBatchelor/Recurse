const audioContext = new AudioContext();
let SingerNode = null;

class VocalChordsWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
    }

    set_tempo(tempo) {
        this.port.postMessage({type: "tempo", data: tempo});
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
    // const controls = document.getElementById('controls');
    // tempo = addHorizSlider("tempo", 40, 200, 100, 1,
    //     (value) => {
    //         if (SingerNode !== null) {
    //             SingerNode.set_tempo(value);
    //         }
    //     });

    // controls.appendChild(tempo);
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
