function sketch(p) {
    circ = [50.0, 50.0];
    circRad = 50;
    circVelocity = [800.0, 800.0];
    circAccel = 8.0;
    i = 0;
    width = 400;
    height = 680;
    // Declare the setup() method.
    p.setup = function () {
        p.createCanvas(width, height);
        p.describe('A white circle drawn on a gray background.');
    };

    function getDistance(x, y) {
        let dx = x - circ[0];
        let dy = y - circ[1];
        let dist = Math.sqrt(dx*dx + dy*dy);
    }

    function intersection(x, y) {
        let dx = circ[0] - x;
        let dy = circ[1] - y;

        let dist = Math.sqrt(dx*dx + dy*dy);


        if (dist > circRad) return;

        let newVel = [0, 0];

        console.log("inside the circle");

        newVel[0] = dx / dist;
        newVel[1] = dy / dist;


        circVelocity[0] += newVel[0] * 100;
        circVelocity[1] += newVel[1] * 100;
    }

    function checkWalls() {
        // check north wall
        if ((circ[1] - circRad) < 0) {
            circ[1] = circRad;
            circVelocity[1] *= -1;
        }
        
        // check east wall
        if ((circ[0] + circRad) > width) {
            circ[0] = width - circRad;
            //console.log(circVelocity);
            circVelocity[0] *= -1;
            //console.log(circVelocity);
        }
       
        // check south wall
        if ((circ[1] + circRad) > height) {
            circ[1] = height - circRad;
            circVelocity[1] *= -1;
        }
        
        // check west wall
        if ((circ[0] - circRad) < 0) {
            circ[0] = circRad;
            circVelocity[0] *= -1;
        }
    }

    // Declare the draw() method.
    p.draw = function () {
        p.background(200);

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
        console.log("pressed! " + p.mouseX + " " + p.mouseY);
        intersection(p.mouseX, p.mouseY); 
    }
}

// Select the web page's body element.
//let body = document.querySelector('body');
let body = document.getElementById('sketch');

// Initialize the sketch and attach it to the web page's body.
new p5(sketch, body);
