function sketch(p) {
    circ = [50.0, 50.0];
    circRad = 50;
    circVelocity = [10.0, 10.0];
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
        return getDistance(x, y);
    }

    function checkWalls() {
        // check north wall
        
        // check east wall
        if ((circ[0] + circRad) > width) {
            circ[0] = width - circRad;
            circVelocity[0] *= -1;
        }
       
        // check south wall
        
        // check west wall
    }

    // Declare the draw() method.
    p.draw = function () {
        p.background(200);

        let ds = p.deltaTime * 0.001;
        // Draw the circle.
        p.circle(circ[0], circ[1], circRad);

        circ[0] += circVelocity[0];
        circ[1] += circVelocity[1];

        circVelocity[0] -= circAccel*ds;
        circVelocity[1] -= circAccel*ds;

        if (circVelocity[0] < 0) circVelocity[0] = 0;
        if (circVelocity[1] < 0) circVelocity[1] = 0;

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
