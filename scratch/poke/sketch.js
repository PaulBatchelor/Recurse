const audioContext = new AudioContext();
let ChatterNode = null;
audioStarted = false

class ChatterWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
    }

    poke(tempo) {
        this.port.postMessage({type: "poke"});
    }
}

const startAudio = async (context) => {
    try {
        await context.audioWorklet.addModule('chatter.js');
    } catch(e) {
        throw new Error(`noise generator error: ${e.message}`);
    }

    const wasmFile = await fetch('dsp.wasm');
    const wasmBuffer = await wasmFile.arrayBuffer();

    const options = {
        wasmBytes: wasmBuffer
    };
    const nd = new
        ChatterWorkletNode(context, 'chatter', {
            processorOptions: options
        });

    nd.connect(context.destination);
    ChatterNode = nd;
};

async function beginAudio() {
    await startAudio(audioContext);
    audioContext.resume();
    audioStarted = true;
}

function sketch(p) {
    circRad = 50;
    circVelocity = [0, 0];
    circAccel = 8.0;
    i = 0;
    width = 400;
    height = 680;
    pokeForce = 200.;
    strokeThickness = 3.
    circ = [width*0.5, height*0.5];

    // Declare the setup() method.
    p.setup = function () {
        p.createCanvas(width, height);
    };

    function poke() {
        console.log("poke");
        if (ChatterNode != null) {
            ChatterNode.poke();
        }
    }

    function getDistance(x, y) {
        let dx = x - circ[0];
        let dy = y - circ[1];
        let dist = Math.sqrt(dx*dx + dy*dy);
    }

    function checkIntersection(x, y) {
        if (audioStarted == false) return;
        let dx = circ[0] - x;
        let dy = circ[1] - y;

        let dist = Math.sqrt(dx*dx + dy*dy);

        if (dist > circRad) return;

        poke();

        let newVel = [0, 0];

        newVel[0] = dx / dist;
        newVel[1] = dy / dist;

        circVelocity[0] += newVel[0] * pokeForce;
        circVelocity[1] += newVel[1] * pokeForce;
    }

    function checkWalls() {
        let strokedWidth = width - strokeThickness;
        let strokedHeight = height - strokeThickness;
        // check north wall
        if ((circ[1] - circRad) < 0) {
            circ[1] = circRad + strokeThickness;
            circVelocity[1] *= -1;
        }

        // check east wall
        if ((circ[0] + circRad) > strokedWidth) {
            circ[0] = strokedWidth - circRad;
            circVelocity[0] *= -1;
        }

        // check south wall
        if ((circ[1] + circRad) > strokedHeight) {
            circ[1] = strokedHeight - circRad;
            circVelocity[1] *= -1;
        }

        // check west wall
        if ((circ[0] - circRad) < 0) {
            circ[0] = circRad + strokeThickness;
            circVelocity[0] *= -1;
        }
    }

    // Declare the draw() method.
    p.draw = function () {
        p.background(255);

        p.strokeWeight(strokeThickness);
        p.rect(3, 3, width -6, height - 6);
        if (audioStarted == false) {
            p.textSize(20);
            p.textAlign(p.CENTER);
            p.text("Tap to begin", width/2, height/2);
            return;
        }

        let ds = p.deltaTime * 0.001;
        // Draw the circle.
        p.circle(circ[0], circ[1], circRad*2.0);

        circ[0] += circVelocity[0]*ds;
        circ[1] += circVelocity[1]*ds;

        //circVelocity[0] -= circAccel*ds;
        //circVelocity[1] -= circAccel*ds;

        circVelocity[0] *= 0.99;
        circVelocity[1] *= 0.99;

        //if (circVelocity[0] < 0) circVelocity[0] = 0;
        //if (circVelocity[1] < 0) circVelocity[1] = 0;

        checkWalls();

    };

    p.mousePressed = function() {
        if (audioStarted == false) {
            //beginAudio();
            return;
            // circ[0] = p.mouseX;
            // circ[1] = p.mouseY;
        }
        checkIntersection(p.mouseX, p.mouseY);
    }
}

// Select the web page's body element.
//let body = document.querySelector('body');
let canvas = document.getElementById('sketch');

canvas.addEventListener('click', async () => {
    if (audioStarted === false) {
        audioStarted = true;
        await startAudio(audioContext);
        audioContext.resume();
    }
})

// Initialize the sketch and attach it to the web page's body.
new p5(sketch, canvas);
