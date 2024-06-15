const audioContext = new AudioContext();
let SingerNode = null;

class GestureDemoWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
        //this.port.onmessage = (event) => this.onmessage(event.data);
        // this.data = {}
        // this.data.regions = [];
        // this.set_pitch(63);
        // for (let i = 0; i < 8; i++) {
        //     this.data.regions.push(0.0);
        //     this.set_region(i + 1, 0.5);
        // }
        // this.set_aspiration(0.1);
        // this.set_noise_floor(0.1);
        // this.set_shape(0.4);
        // this.set_velum(0.0);
    }

    set_pitch(pitch) {
        this.data.pitch = parseFloat(pitch);
        this.port.postMessage({type: "pitch", data: pitch});
    }

    set_region(region, value) {
        this.data.regions[region - 1] = parseFloat(value);
        this.port.postMessage({
            type: "regset",
            region: region,
            value: value,
        });
    }

    set_aspiration(aspiration) {
        this.data.aspiration = parseFloat(aspiration);
        this.port.postMessage({type: "aspiration", data: aspiration});
    }

    set_noise_floor(noise_floor) {
        this.data.noise_floor = parseFloat(noise_floor);
        this.port.postMessage({type: "noise_floor", data: noise_floor});
    }

    set_shape(shape) {
        this.data.shape = shape;
        this.port.postMessage({type: "shape", data: shape});
    }

    set_velum(velum) {
        this.data.velum = velum;
        this.port.postMessage({type: "velum", data: velum});
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

const startAudio = async (context) => {
    try {
        await context.audioWorklet.addModule('gesture_demo.js');
    } catch(e) {
        throw new Error(`noise generator error: ${e.message}`);
    }

    const wasmFile = await fetch('dsp.wasm');
    const wasmBuffer = await wasmFile.arrayBuffer();

    const options = {
        wasmBytes: wasmBuffer
    };
    const Singer = new
        GestureDemoWorkletNode(context, 'singer', {
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
});
