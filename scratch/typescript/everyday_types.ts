// vim:sw=4:ts=4:et
//
let s: string = "hello";
let b: boolean = false;
let x: number = 666;
let a: number[] = [2, 4, 6];
let z: string[] = ["one", "two", "three"]

let obj: any = { x: 0 }

obj.foo();
obj();
obj.bar = 100;
obj = "hello";
const n: number = obj;

let myName = "Alice";

function greet2(name: string) {
    console.log("Hello " + name.toUpperCase() + "!!");
}

// greet2(42);

function getFavoriteNumber(): number {
    return 26;
}

//let fave: string = getFavoriteNumber();
let fave = getFavoriteNumber();

// contextual typing
{
    const names = ["Alice", "Bob", "Eve"];

    names.forEach(function (s) {
        console.log(s.toUpperCase());
    })

    names.forEach((s) => s.toUpperCase());
}

function printCoord(pt: { x: number; y: number }) {
    console.log(`${pt.x}, ${pt.y}`);
}

printCoord({ x: 1, y: 2 })
// printCoord({ x: 1, y: 2, z: 3 })

function printName(obj: { first: string; last?: string }) {
    if (obj.last !== undefined) {
        console.log(obj.last.toUpperCase);
    }

    console.log(obj.last?.toUpperCase);
}

printName({ first: "will" })
printName({ first: "will", last: "smith" })

function printId(id: number | string) {
    console.log("Your id is " + id);
    // console.log(id.toUpperCase());

    if (typeof id == "string") {
        console.log(id.toUpperCase());
    } else {
        console.log(id);
    }
}

printId(101);
printId("42");

// printId({ myid: 1234 });

function welcomePeople(x: string[] | string) {
    if (Array.isArray(x)) {
        console.log("Welcome " + x.join(" and "));
    } else {
        console.log("Welcome lone traveler" + x);
    }
}

function getFirstThree(x: number[] | string[]) {
    return x.slice(0, 3);
}
{
    type Point = {
        x: number;
        y: number;
    }

    let printCoord = (pt: Point) => {
        console.log("The coordinate's x value is " + pt.x);
        console.log("The coordinate's y value is " + pt.y);
    }

    printCoord({ x: 100, y: 101 });
}

type ID = number | string;

{
    interface Point {
        x: number;
        y: number;
    }

    let printCoord = (pt: Point) => {
        console.log(pt.x, pt.y);
    }

    // structurally typed system: typescript only cares about the "shape"
    // of the data
    printCoord({ x: 100, y: 100 });
}

interface Animal {
    name: string;
}

interface Bear extends Animal {
    honey: boolean;
}
{
    type Animal = {
        name: string;
    }

    type Bear = Animal & {
        honey: boolean;
    }
}

interface Window {
    title: string;
}

interface Window {
    ts: number;
}

{
    // type Window = {
    //     title: string;
    // }

    // type Window = {
    //     ts: number;
    // }
}

// type assertions
const myCanvas = document.getElementById("main_canavs") as HTMLCanvasElement;
const myCanvas2 = <HTMLCanvasElement>document.getElementById("main_canvas");

//const x2 = "hello" as number;

// const a2 = expr as any as T;

// literal types
let changingString = "Hello World";

changingString = "Hello Another World";

const constantString = "Hello World";

// constantString = "Hello Another World";

function printText(_s: string, _aligment: "left" | "right" | "center") {
    // ...
}

printText("Hello, World", "left");
// printText("G'day, Mate", "centre");


function compare(a: string, b: string): -1 | 0 | 1 {
    return a == b ? 0 : a > b ? 1 : -1;
}

interface Options {
    width: number;
}

function configure(_x: Options | "auto") {
    // ...
}

configure({ width: 100 });
configure("auto");
//configure("automatic");

// literal inference
declare function handleRequest(url: string, method: "GET" | "POST"): void;

const req = { url: "https://example.com", method: "GET" };
//handleRequest(req.url, req.method);
handleRequest(req.url, req.method as "GET");

const req2 = { url: "https://example.com", method: "GET" } as const;
handleRequest(req2.url, req2.method);

// non-null assertion operator postfix

function liveDangerously(x?: number | null) {
    console.log(x!.toFixed());
}

// less common primitives
let oneHundred: bigint = BigInt(100);

// es2020 onwards
// let anotherHundred: bigint = 100n;

const firstName = Symbol("name");
const secondName = Symbol("name");

// if (firstName === secondName) {
// 
// }
