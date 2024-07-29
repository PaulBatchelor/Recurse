function sketch(p) {
	let width = 400
	let height = 680
	let circWidth = width * 0.2
	let xPos = -1
	let yPos = -1
	let noteOn = false


	p.setup = function() {
		p.createCanvas(width, height)
	}

 	function gateOn() {
		console.log("on")
	}
	
	function gateOff() {
		console.log("off")
	}

	function clamp(x, mn, mx) {
		x = x > mx  ? mx : x;
		x = x < mn ? mn : x;
		return x
	}

	function move(x, y) {
		let x_norm = clamp(x/width, 0, 1)
		let y_norm = clamp(y/height, 0, 1)
		// TODO: don't send if there aren't any changes
		//console.log(x_norm, y_norm)
	}

	p.draw = function () {
		p.background(0, 128, 128)
		p.fill(255)
		p.noStroke()
		if (noteOn) {
			let x = p.mouseX
			let y = p.mouseY
			p.circle(x, y, circWidth)
			move(x, y)
		}
	}

	p.mousePressed = function() {
		noteOn = true
		gateOn()
	} 

	p.mouseReleased = function() {
		noteOn = false
		gateOff()
	}
}

export { sketch }
