const canvas = document.getElementById('canvas');
const html = document.getElementsByTagName('html')[0];
const container = document.getElementById('container');

canvas.width = 400;
canvas.height = 400;

let ctx = canvas.getContext('2d');

var clickPoint = [-1, -1];
var originPoint = [-1, -1];
var avatarPos = [-1, -1];
var travelVector = [-1, -1];
var isMoving = false;

function validPoint(point) {
    return point[0] >= 0 && point[1] >= 0;
}

function closeEnough(pointA, pointB) {
    let distX = pointB[0] - pointA[0];
    let distY = pointB[1] - pointA[1];

    let dist = Math.sqrt(distX*distX + distY*distY);
    return dist < 2;
}

var lastTimeStamp;

function draw(timeStamp) {
    var dt = 0;

    timeStamp *= 0.001;
    if (lastTimeStamp) {
        dt = timeStamp - lastTimeStamp;
    }

    lastTimeStamp = timeStamp;

    canvas.width = html.clientWidth;
    canvas.height = html.clientHeight;

    ctx.fillStyle = '#FFF'
    ctx.lineWidth = 10;
    ctx.strokeStyle = '#000';

    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (!validPoint(avatarPos)) {
        avatarPos[0] = canvas.width / 2;
        avatarPos[1] = canvas.height / 2;
    }

    ctx.beginPath();
    ctx.arc(
        avatarPos[0],
        avatarPos[1],
        100,
        0, 2.0 * Math.PI, true
    );
    ctx.closePath();
    ctx.stroke()
    ctx.fill();

    if (validPoint(clickPoint)) {
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(
            clickPoint[0],
            clickPoint[1],
            25,
            0, 2.0 * Math.PI, true
        );
        ctx.closePath();
        ctx.fill();
    }

    if (isMoving) {
        avatarPos[0] += travelVector[0]*dt;
        avatarPos[1] += travelVector[1]*dt;

        if (closeEnough(avatarPos, clickPoint)) {
            isMoving = false;
        }
    }

    let raf = window.requestAnimationFrame(draw);
}

function down(event) {
    clickPoint = [event.clientX, event.clientY];
    originPoint = avatarPos.slice();

    let distX = clickPoint[0] - originPoint[0];
    let distY = clickPoint[1] - originPoint[1];

    travelVector = [distX, distY];
    isMoving = true;
}

canvas.addEventListener('pointerdown', down, false);

draw();
