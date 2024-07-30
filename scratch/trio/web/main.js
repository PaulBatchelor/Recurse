const canvas = document.getElementById('canvas');
const html = document.getElementsByTagName('html')[0];

canvas.width = 500;
canvas.height = 500;
const ctx = canvas.getContext('2d');

let gate=false
let circX = -1;
let circY = -1;
let totalSteps = 8;

function getStepWidth(portraitMode, width, height) {
    if (portraitMode) {
        return canvas.height / totalSteps;
    }

    return canvas.width / totalSteps;
}

function draw() {
    //canvas.width = window.innerWidth;
    //canvas.height = window.innerHeight;
    canvas.width = html.clientWidth;
    canvas.height = html.clientHeight;
    ctx.fillStyle = '#008080';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.lineWidth = 3;
    ctx.strokeStyle = '#FFF';

    let portraitMode = canvas.height > canvas.width;

    let stepWidth = getStepWidth(portraitMode, canvas.width, canvas.height);

    for (i = 1; i < totalSteps; i++) {
        if (portraitMode) {
            ctx.beginPath();
            ctx.moveTo(0, i*stepWidth);
            ctx.lineTo(canvas.width, i*stepWidth);
            ctx.closePath();
            ctx.stroke();
        } else {
            ctx.beginPath();
            ctx.moveTo(i*stepWidth, 0);
            ctx.lineTo(i*stepWidth, canvas.height);
            ctx.closePath();
            ctx.stroke();
        }
    }
   
    ctx.fillStyle = '#FFFFFF';
    if (gate && circX >= 0 && circY >= 0) {
        ctx.beginPath();
        ctx.arc(circX, circY, 50, 0, 2 * Math.PI, true);
        ctx.closePath();
        ctx.fill();
    }


    raf = window.requestAnimationFrame(draw);
}

function down(event) {
    circX = event.clientX;
    circY = event.clientY;
    gate = true;
    console.log('down');
}

function up(event) {
    gate = false;
    console.log('up');
        
}

function move(event) {
    circX = event.clientX;
    circY = event.clientY;
}

// canvas.addEventListener('mousedown', down);
// canvas.addEventListener('mousemove', move);
// canvas.addEventListener('mouseup', up);

canvas.addEventListener('pointerdown', down, false);
canvas.addEventListener('pointermove', move, false);
canvas.addEventListener('pointerup', up, false);

draw();
