// From https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html
// vim:sw=4:ts=4
let helloWorld = "Hello World";

const user = {
    name: "Hayes",
    id: 0,
}

interface User {
    name: string;
    id: number;
}

const user2: User = {
    name: "Hayes",
    id: 0
}

class UserAccount {
    name: string;
    id: number;

    constructor(name: string, id: number) {
        this.name = name;
        this.id = id;
    }
}

const user3: User = new UserAccount("Murphy", 1);

function deleteUser(user: User) {

}

// function getAdminUser(): User {
// 
// }

type MyBool = true | false;

type WindowStates = "open" | "closed" | "minimized";
type LockStates = "locked" | "unlocked";
type PositiveOddNumbersUnderTen = 1 | 3 | 5 | 7 | 9;

function getLength(obj: string | string[]) {
    return obj.length;
}

function wrapInArray(obj: string | string[]) {
    if (typeof obj === "string") {
        return [obj]
    }

    return obj;
}

type StringArray = Array<string>;
type NumberArray = Array<number>;
type ObjectWithNameArray = Array<{ name: string }>;

interface Backpack<Type> {
    add: (obj: Type) => void;
    get: () => Type;
}

declare const backpack: Backpack<string>;

const object = backpack.get();

backpack.add("23");

interface Point {
    x: number;
    y: number;
}

function logPoint(p: Point) {
    console.log(`${p.x}, ${p.y}`);
}

const point = { x: 12, y: 26 };
logPoint(point);

const point3 = { x: 12, y: 26, z: 4 };
logPoint(point3);

class VirtualPoint {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
}

const newPoint = new VirtualPoint(1, 2);
logPoint(newPoint);

function greet(person: string, date: Date) {
    console.log(`hello ${person}, today is ${date.toDateString}`);
}

//greet("Maddison", Date());
greet("Maddison", new Date());

