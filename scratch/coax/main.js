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
var movementPos = 0;

function validPoint(point) {
    return point[0] >= 0 && point[1] >= 0;
}

var incrementAmount = 0;
var incrementSpeed = 1.0;


function calcDist(pointA, pointB) {
    let distX = pointB[0] - pointA[0];
    let distY = pointB[1] - pointA[1];

    let dist = Math.sqrt(distX*distX + distY*distY);
    return dist;
}
function closeEnough(pointA, pointB) {
    let dist = calcDist(pointA, pointB);
    return dist <= 5;
}

function calcProgress(origin, current, target) {
    let distOrigTarg = calcDist(origin, target);
    let distOrigCurr= calcDist(origin, current);

    return distOrigCurr/distOrigTarg;
}

function lerp(pointA, pointB, amount) {
    return [
        (1-amount)*pointA[0] + amount*pointB[0],
        (1-amount)*pointA[1] + amount*pointB[1],
    ];
}

function cubicEaseIn(x) {
    return x * x * x;
}

function cubicEaseOut(x) {
    return 1.0 - Math.pow(1.0 - x, 3);
}

function linear(x) {
    return x;
}

let movementBehaviors = [
    cubicEaseIn,
    cubicEaseOut,
    linear,
];

var currentBehavior = movementBehaviors[0];

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

        let prog = calcProgress(originPoint, avatarPos, clickPoint);
        prog = prog * prog * prog;
        let speed = prog*500 + (1 - prog)*200;
        //avatarPos[0] += travelVector[0]*dt*speed;
        //avatarPos[1] += travelVector[1]*dt*speed;
        //let behavior = cubicEaseIn;
        //let behavior = linear;
        //let behavior = cubicEaseOut;
        avatarPos = lerp(originPoint, clickPoint, currentBehavior(movementPos));

        movementPos += dt * incrementSpeed;

        if (movementPos > 1.0) {
            isMoving = false;
        }

        // if (closeEnough(avatarPos, clickPoint)) {
        //     isMoving = false;
        // }
    }

    let raf = window.requestAnimationFrame(draw);
}

function down(event) {
    clickPoint = [event.clientX, event.clientY];
    originPoint = avatarPos.slice();

    let dist = calcDist(originPoint, clickPoint);

    let distX = clickPoint[0] - originPoint[0];
    let distY = clickPoint[1] - originPoint[1];

    let absDistX = Math.abs(distX);
    let absDistY = Math.abs(distY);

    let largestDist = absDistX > absDistY ? absDistX : absDistY;

    console.log(dist);

    incrementSpeed = (Math.random() * 500 + 500.0) / dist;

    movementPos = 0;
    travelVector = [distX / largestDist, distY / largestDist];
    isMoving = true;

    let behaviorIdx = Math.floor(movementBehaviors.length * Math.random());
    currentBehavior = movementBehaviors[behaviorIdx];
}

canvas.addEventListener('pointerdown', down, false);

draw();
