const audioContext = new AudioContext();
let SingerNode = {}; 

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
};

const pitch_slider = document.getElementById('pitch');
const pitch_value = document.getElementById('pitch-value');
pitch_value.textContent = pitch_slider.value;

pitch_slider.addEventListener("input", (event) => {
    pitch_value.textContent = event.target.value;
    SingerNode.set_pitch(event.target.value);
});

// TODO: refactor

const rnum = 1
const region_slider = document.getElementById('region1');
const region_value = document.getElementById('region1-value');
region_value.textContent = pitch_slider.value;

region_slider.addEventListener("input", (event) => {
    pitch_value.textContent = event.target.value;
    SingerNode.set_region(1, event.target.value);
});

window.addEventListener('load', async () => {
  const buttonStart = document.getElementById('button-start');
  const buttonStop = document.getElementById('button-stop');
  const buttonBegin = document.getElementById('button-begin');
  console.log(audioContext.state);
  buttonBegin.disabled = false;
  buttonStart.disabled = true;
  buttonBegin.addEventListener('click', async () => {
      await startAudio(audioContext);
      audioContext.resume();
      buttonBegin.disabled = true;
      buttonBegin.textContent = 'Playing...';
      buttonStart.disabled = true;
      buttonStop.disabled = false;
  }, false);
  buttonStop.addEventListener('click', async () => {
      audioContext.suspend();
      buttonStart.disabled = false;
      buttonStop.disabled = true;
  }, false);

  buttonStart.addEventListener('click', async () => {
      audioContext.resume();
      buttonStart.disabled = true;
      buttonStop.disabled = false;
  }, false);
});
