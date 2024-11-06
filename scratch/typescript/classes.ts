// class Point {
//     x: number;
//     y: number;
// }

class Point {
    x = 0;
    y = 0;
}

const pt = new Point();

pt.x = 0;
pt.y = 0;

class goodGreeter {
    name: String;
    constructor() {
        this.name = "hello";
    }
}

class OKGreeter {
    name!: String;
}

class Greeter {
    readonly name: string = "world";

    constructor(otherName?: string) {
        if (otherName !== undefined) {
            this.name = otherName;
        }
    }

    err() {
        // this.name = "other name";
    }
}

let g = new Greeter();
// g.name = "also not okay";

// Constructors

class Point2 {
    x: number = 0;
    y: number = 0;

    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }

    // constructor overloads
    // constructor(x: number, y: number);
    // constructor(xy: string);
    // constructor(x: string | number, y: number = 0) {
    //     // code logic here
    // }
}

// super calls
class Base {
    k = 4;
}

class Derived extends Base {
    constructor() {
        super();
        console.log(this.k);
    }
}

class Point3 {
    x = 10;
    y = 10;

    scale(n: number): void {
        this.x *= n;
        this.y *= n;
    }
}

// setters/getters

class C {
    _length = 0;

    get length() {
        return this._length;
    }

    set length(value) {
        this._length = value;
    }
}

class Thing {
    _size = 0;

    get size(): number {
        return this._size;
    }

    set size(value: string | number | boolean) {
        let num = Number(value);

        if (!Number.isFinite(num)) {
            this._size = 0;
            return;
        }

        this._size = num;
    }
}

// index signatures

class MyClass {
    [s: string]: boolean | ((s: string) => boolean);

    check(s: string) {
        return this[s] as boolean;
    }
}

// class heritage

interface Pingable {
    ping(): void;
}

class Sonar implements Pingable {
    ping() {
        console.log("ping!");
    }
}

// class Ball implements Pingable {
//     pong() {
//         console.log("pong!");
//     }
// }

// Cautions
