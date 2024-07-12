const AudioContext = window.AudioContext || window.webkitAudioContext;

const audioContext = new AudioContext();
let ChatterNode = null;
audioStarted = false

class ChatterWorkletNode extends AudioWorkletNode {
    constructor(context, name, options) {
        super(context, name, options);
        this.port.onmessage = (event) => this.onmessage(event.data);
        this.mouthopen = 0.;
        this.mouthState = [0, 0, 0.0];
    }

    poll() {
        this.port.postMessage({type: "mouthopen-get"});
        this.port.postMessage({type: "mouthstate-get"});
    }

    poke(tempo) {
        this.port.postMessage({type: "poke"});
    }

    onmessage(event) {
        if (event.type === "mouthstate-rsp") {
            this.mouthState = event.data.slice();
        } else if (event.type === "mouthopen-rsp") {
            this.mouthopen = event.data;
        }
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

    pokeExpand = 2.0;

    let mouthShapes = [
        [1.0, 0.5, 0.0, 0.0],
        [0.5, 1.0, 0.0, 0.0],
        [0.5, 0.5, 0.0, 0.0],
        [1.8, 0.2, 0.0, 0.0]
    ];

    var mouthState = [0, 0, 0.0];

    let closedMouth = [1.0, 0.04];

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

    function poll() {
        if (ChatterNode != null) {
            ChatterNode.poll();
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

        if (dist > circRad*pokeExpand) return;

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

    function computeMouthShape() {
        var ms = mouthShapes[0];
        var open = 1.0;

        if (ChatterNode != null) {
            open = ChatterNode.mouthopen;
            let state = ChatterNode.mouthState;

            let shp1 = mouthShapes[state[0]];
            let shp2 = mouthShapes[state[1]];
            let pos = state[2];

            ms = [
                (1.0 - pos)*shp1[0] + pos*shp2[0],
                (1.0 - pos)*shp1[1] + pos*shp2[1]
            ];

        }

        return [
            open*ms[0] + (1.0 - open)*closedMouth[0],
            open*ms[1] + (1.0 - open)*closedMouth[1]
        ];
    }

    // Declare the draw() method.
    p.draw = function () {
        p.fill(255);
        p.background(255);
        p.strokeWeight(strokeThickness);

        if (audioStarted == false) {
            p.fill(0, 0, 0, 0);
            p.rect(strokeThickness*0.5, strokeThickness*0.5, width - strokeThickness, height - strokeThickness);
            p.fill(0);
            p.textSize(20);
            p.textAlign(p.CENTER);
            p.text("Tap to begin (Warning: loud sound)", width/2, height/2);
            return;
        }

        poll();

        let ds = p.deltaTime * 0.001;

        p.fill(255);
        // Face
        p.circle(circ[0], circ[1], circRad*2.0);

        // eyes
        p.circle(circ[0] - circRad*0.6, circ[1] - circRad*0.4, circRad*1.0);
        p.circle(circ[0] + circRad*0.6, circ[1] - circRad*0.4, circRad*1.0);

        p.fill(0);
        p.circle(circ[0] - circRad*0.6, circ[1] - circRad*0.4, circRad*0.2);
        p.circle(circ[0] + circRad*0.6, circ[1] - circRad*0.4, circRad*0.2);

        // mouth
        let ms = computeMouthShape();

        p.ellipse(circ[0], circ[1] + circRad*0.6, circRad * ms[0], circRad * ms[1]);

        circ[0] += circVelocity[0]*ds;
        circ[1] += circVelocity[1]*ds;

        circVelocity[0] *= 0.99;
        circVelocity[1] *= 0.99;

        checkWalls();
        p.fill(0, 0, 0, 0);
        p.rect(strokeThickness*0.5, strokeThickness*0.5, width - strokeThickness, height - strokeThickness);

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

let canvas = document.getElementById('sketch');

canvas.addEventListener('click', async () => {
    if (audioStarted === false) {
        audioStarted = true;
        await startAudio(audioContext);
        audioContext.resume();
    }
})

new p5(sketch, canvas);
