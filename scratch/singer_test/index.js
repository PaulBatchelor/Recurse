const audioContext = new AudioContext();
let SingerNode = null;

class SingerWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
        //this.port.onmessage = (event) => this.onmessage(event.data);
    }

    set_pitch(pitch) {
        this.port.postMessage({type: "pitch", data: pitch});
    }

    set_region(region, value) {
        this.port.postMessage({
            type: "regset",
            region: region,
            value: value,
        });
    }

    set_aspiration(aspiration) {
        this.port.postMessage({type: "aspiration", data: aspiration});
    }

    set_noise_floor(noise_floor) {
        this.port.postMessage({type: "noise_floor", data: noise_floor});
    }

    set_shape(shape) {
        this.port.postMessage({type: "shape", data: shape});
    }
}

const startAudio = async (context) => {
    try {
        await context.audioWorklet.addModule('singer.js');
    } catch(e) {
        throw new Error(`noise generator error: ${e.message}`);
    }

    const wasmFile = await fetch('dsp.wasm');
    const wasmBuffer = await wasmFile.arrayBuffer();

    const options = {
        wasmBytes: wasmBuffer
    };
    const Singer = new
        SingerWorkletNode(context, 'singer', {
            processorOptions: options
        });

    Singer.connect(context.destination);
    SingerNode = Singer;

    for (let i = 1; i <= 8; i++) {
        SingerNode.set_region(i, 0.5);
        const rslider = document.getElementById('region' + i);
        const rvalue = document.getElementById('region' + i + '-value');
        rslider.value = 0.5;
        rvalue.textContent = "0.5";
    }
};

function add_region_slider(sliders, rnum) {
    const region = document.createElement('p')
    region.textContent = 'R' + rnum + ': ';
    const slider = document.createElement('input');
    const output = document.createElement('output');

    slider.type = "range";
    slider.min = 0;
    slider.max = 1;
    slider.id = 'region' + rnum;
    slider.step = 0.001;
    slider.value = 0.5;

    output.id = 'region' + rnum + '-value';
    output.textContent = slider.value;

    slider.addEventListener("input", (event) => {
        output.textContent = event.target.value;
        if (SingerNode !== null) {
            SingerNode.set_region(rnum, event.target.value);
        }
    });

    region.appendChild(slider);
    region.appendChild(output);
    sliders.appendChild(region);
}

function add_region_sliders() {
    const sliders = document.getElementById('region-sliders');

    for (let i = 1; i <= 8; i++) {
        add_region_slider(sliders, i);
    }
}

// https://stackoverflow.com/questions/1026069/how-do-i-make-the-first-letter-of-a-string-uppercase-in-javascript
function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
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

function add_glottal_controls() {
    const glottal_control = document.getElementById('glottal-control');
    pitch = addHorizSlider("pitch", 50, 80, 65, 1,
        (value) => {
            if (SingerNode !== null) {
                SingerNode.set_pitch(value);
            }
        });

    aspiration = addHorizSlider("aspiration", 0, 1, 0.03, 0.001,
        (value) => {
            if (SingerNode !== null) {
                SingerNode.set_aspiration(value);
            }
        });

    noise_floor = addHorizSlider("noise_floor", 0, 1, 0.01, 0.001,
        (value) => {
            if (SingerNode !== null) {
                SingerNode.set_noise_floor(value);
            }
        });

    shape = addHorizSlider("shape", 0.1, 0.9, 0.4, 0.001,
        (value) => {
            if (SingerNode !== null) {
                SingerNode.set_shape(value);
            }
        });
    glottal_control.appendChild(pitch);
    glottal_control.appendChild(shape);
    glottal_control.appendChild(aspiration);
    glottal_control.appendChild(noise_floor);
}

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
    add_glottal_controls();
    add_region_sliders();
});
