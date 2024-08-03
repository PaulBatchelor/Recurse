const canvas = document.getElementById('canvas');
const html = document.getElementsByTagName('html')[0];
const container = document.getElementById('container');

canvas.width = 400;
canvas.height = 400;

let ctx = canvas.getContext('2d');

var clickPoint = [-1, -1];
let pointPool = [];
var originPoint = [-1, -1];
var avatarPos = [-1, -1];
var isMoving = false;
var movementPos = 0;
var waitTimer = 0;
var blobScale = 1.0;
var blobScaleTarget = 1.0;
var pleaseShrink = false;
var idleTimer = 0;
var pleaseDigest = false;
let blobScaleMax = 3.0;

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
    let distOrigCurr = calcDist(origin, current);

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

function updateTrajectory(origin, point) {
    let dist = calcDist(origin, point);

    incrementSpeed = (Math.random() * 500 + 500.0) / dist;

    movementPos = 0;
    isMoving = true;

    let behaviorIdx = Math.floor(movementBehaviors.length * Math.random());
    currentBehavior = movementBehaviors[behaviorIdx];
}

function drawPellet(point) {
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(
        point[0],
        point[1],
        25,
        0, 2.0 * Math.PI, true
    );
    ctx.closePath();
    ctx.fill();
}

var lfoPhase = 0;
function drawAvatar(dt) {
    var wiggle = 1.0;
    if (!pleaseDigest && !pleaseShrink && blobScale >= blobScaleMax * 0.8) {
        let lfo = Math.sin(2.0*Math.PI*lfoPhase);
        lfoPhase += dt * 6;
        if (lfoPhase > 1.0) {
            lfoPhase -= 1.0;
        }
        wiggle += 0.05*lfo;

    }
    ctx.fillStyle = '#FFF'
    ctx.lineWidth = 10;
    ctx.strokeStyle = '#000';
    ctx.beginPath();
    ctx.arc(
        avatarPos[0],
        avatarPos[1],
        50 * blobScale * wiggle,
        0, 2.0 * Math.PI, true
    );
    ctx.closePath();
    ctx.fill();
    ctx.stroke()
}

function lerper(a, b, t) {
    return (a + (b - a)*t);
}

function getPoint(origin) {
    return pointPool.pop();
}

function insertPoint(x, y) {

}

function draw(timeStamp) {
    var dt = 0;

    timeStamp *= 0.001;
    if (lastTimeStamp) {
        dt = timeStamp - lastTimeStamp;
    }

    lastTimeStamp = timeStamp;

    if (waitTimer <= 0 && !isMoving && pointPool.length > 0) {
        originPoint = avatarPos.slice();
        clickPoint = getPoint(originPoint);
        updateTrajectory(originPoint, clickPoint);
        blobScaleTarget *= 1.1;

        if (blobScale > blobScaleMax) {
            pleaseShrink = true;
        }

        idleTimer = 0;
    } else if (!isMoving) {
        idleTimer += dt;
    }

    pleaseDigest = idleTimer > 2;

    blobScale = lerper(blobScale, blobScaleTarget, 0.9*dt);

    if (blobScale < 1.0) {
        blobScale = 1.0;
    }

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

    if (validPoint(clickPoint)) {
        drawPellet(clickPoint);

    }
    for (let i = 0; i < pointPool.length; i++) {
        drawPellet(pointPool[i]);
    }

    if (isMoving && !pleaseShrink) {
        let prog = calcProgress(originPoint, avatarPos, clickPoint);
        prog = prog * prog * prog;
        let speed = prog*500 + (1 - prog)*200;
        avatarPos = lerp(originPoint, clickPoint, currentBehavior(movementPos));

        movementPos += dt * incrementSpeed;

        if (movementPos > 1.0) {
            isMoving = false;
            clickPoint = [-1, -1];
            let waitAndDigestPellet = Math.random() > 0.6;
            if (waitAndDigestPellet) {
                waitTimer = Math.random() * 1;
            }
        }
    } else if (waitTimer > 0) {
        waitTimer -= dt;
    }

    if (pleaseDigest && blobScaleTarget > 1.0) {
        blobScaleTarget -= 3*dt;
    }

    if (pleaseShrink) {
        if (blobScaleTarget > 1.0) {
            blobScaleTarget -= 2*dt;
        }
        if (blobScale <= 1.0) {
            pleaseShrink = false;
            waitTimer = 1.0;
        }
    }

    drawAvatar(dt);

    let raf = window.requestAnimationFrame(draw);
}


function down(event) {
    if (pointPool.length < 16) {
        pointPool.push([event.clientX, event.clientY]);
    }
}

canvas.addEventListener('pointerdown', down, false);

draw();
