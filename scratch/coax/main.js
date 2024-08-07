const BGCOLOR='#a8f8f8';
//const COLOR_AVATAR='#f8a0d8';
const COLOR_AVATAR='#ffffff';
//const COLOR_PELLET='#f8d000';
//const COLOR_PELLET='#f83830';
//
const AVATAR_LINE_THICKNESS = 5;
const PELLET_LINE_THICKNESS = 5;
const COLOR_PELLET='#f8a0d8';
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
const MAX_PELLETS = 16;
var numPoints = 0;

function validPoint(point) {
    return point[0] >= 0 && point[1] >= 0;
}

var incrementAmount = 0;
var incrementSpeed = 1.0;

function poolHasRoom() {
    return numPoints < MAX_PELLETS;
}

function addPoint(x, y) {
    numPoints++;

    if (pointPool.length < MAX_PELLETS) {
        pointPool.push([x, y]);
    } else {
        for (let i = 0; i < MAX_PELLETS; i++) {
            if (!validPoint(pointPool[i])) {
                pointPool[i] = [x, y];
                break;
            }
        }
    }
}

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
    ctx.fillStyle = COLOR_PELLET;
    ctx.lineWidth = PELLET_LINE_THICKNESS;
    ctx.beginPath();
    ctx.arc(
        point[0],
        point[1],
        25,
        0, 2.0 * Math.PI, true
    );
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
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
    ctx.fillStyle = COLOR_AVATAR;
    ctx.lineWidth = AVATAR_LINE_THICKNESS;
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
    numPoints--;
    return pointPool.pop();
}

function getNearestPoint(origin) {
    var minDist;
    var minDistIdx;

    for (let i = 0; i < MAX_PELLETS; i++) {
        if (i < pointPool.length && validPoint(pointPool[i])) {
            let curDist = calcDist(origin, pointPool[i]);
            if (!minDist || (minDist && (curDist < minDist))) {
                minDist = curDist;
                minDistIdx = i;
            }
        }
    }

    let nextPoint = [
        pointPool[minDistIdx][0],
        pointPool[minDistIdx][1]
    ];


    pointPool[minDistIdx] = [-1, -1];
    //return getPoint(origin);
    numPoints--;
    return nextPoint;
}

function draw(timeStamp) {
    var dt = 0;

    timeStamp *= 0.001;
    if (lastTimeStamp) {
        dt = timeStamp - lastTimeStamp;
    }

    lastTimeStamp = timeStamp;

    if (waitTimer <= 0 && !isMoving && numPoints > 0) {
        originPoint = avatarPos.slice();
        clickPoint = getNearestPoint(originPoint);
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

    ctx.fillStyle = BGCOLOR;
    ctx.lineWidth = AVATAR_LINE_THICKNESS;
    ctx.strokeStyle = '#000';

    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (!validPoint(avatarPos)) {
        avatarPos[0] = canvas.width / 2;
        avatarPos[1] = canvas.height / 2;
    }

    if (validPoint(clickPoint)) {
        drawPellet(clickPoint);

    }
    for (let i = 0; i < MAX_PELLETS; i++) {
        if (i < pointPool.length && validPoint(pointPool[i])) {
            drawPellet(pointPool[i]);
        }
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
    if (poolHasRoom()) {
        //pointPool.push([event.clientX, event.clientY]);
        addPoint(event.clientX, event.clientY);
    }
}

canvas.addEventListener('pointerdown', down, false);

draw();
