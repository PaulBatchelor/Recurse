// vim:ts=2:sw=2:et
function greet(person: { name: string; age: number }) {
  console.log("Hello " + person.name);
}

interface Person {
  name: string;
  age: number;
}

type PersonType = {
  name: string;
  age: number;
}

function greet2(person: Person | PersonType) {
  console.log("Hello " + person.name)
}

// Property Modifiers

// Optional Properties

interface Shape {

}

interface PaintOptions {
  shape: Shape;
  xPos?: number;
  yPos?: number;
}

function paintShape(opts: PaintOptions) {
  // ..
  let xPos = opts.xPos;
  console.log(xPos);
}

function paintShape2({ shape, xPos = 0, yPos = 0 }: PaintOptions) {

}

interface SomeType {
  readonly prop: string;
}

function doSomething(obj: SomeType) {
  console.log(`prop has the value ${obj.prop}`);
  // obj.prop = "hello";
}

interface Home {
  readonly resident: { name: string, age: number };
}

function visitForBirthday(home: Home) {
  home.resident.age++;
}

function evict(home: Home) {
  //  home.resident = {
  //    name: "Paul",
  //    age: 10,
  //  };
}

interface Person {
  name: string;
  age: number;
}

interface ReadOnlyPerson {
  readonly name: string;
  readonly age: number;
}

let writeablePerson: Person = {
  name: "Paul",
  age: 123,
};

let readOnlyPerson: ReadOnlyPerson = writeablePerson;

console.log(readOnlyPerson.age);
writeablePerson.age++;
console.log(readOnlyPerson.age);

// Inded Signatures

interface StringArray2 {
  [index: number]: String;
}

interface NumberDictionary {
  [index: string]: number;
  length: number;
  // name: string;
}

interface NumberOrStringDictionary {
  [index: string]: number | string;
  length: number;
  name: string;
}

interface ReadOnlyStringArray {
  readonly [index: number]: string;
}

// Excess Property Checks

interface SquareConfig {
  color?: string;
  width?: number;
}

function createSquare(config: SquareConfig): { color: string, width: number } {
  return {
    color: config.color || "red",
    width: config.width ? config.width * config.width : 20,
  }
}

//createSquare({ colour: "red", width: 100 });
createSquare({ color: "red", width: 100 });

createSquare({ colour: "red", width: 100, opacity: 0.5 } as SquareConfig);

interface SquareConfig2 {
  color?: string;
  width?: number;
  [propName: string]: unknown;
}

// Extending Types

interface BasicAddress {
  name?: string;
  street: string;
  city: string;
  country: string;
  postalCode: string;
}

// interface AddressWithUnit {
//   name?: string;
//   unit: string;
//   street: string;
//   city: string;
//   country: string;
//   postalCode: string;
// }

interface AddressWithUnit extends BasicAddress {
  unit: string;
}

interface Colorful {
  color: string;
}

interface Circle2 {
  radius: number;
}

interface ColorfulCircle extends Colorful, Circle2 { }

const cc: ColorfulCircle = {
  color: "red",
  radius: 42,
}

// Intersection Types

type ColorfulCircle2 = Colorful & Circle2;

function draw(circle: Colorful & Circle2) {
  console.log(`color was ${circle.color}`);
  console.log(`radius was ${circle.radius}`);
}

draw({ color: "blue", radius: 42 })
// draw({ color: "red", raidus: 42 })

// Interface Extension vs Intersection

interface Person1 {
  name: string;
}

interface Person2 {
  name: number;
}

type Staff = Person1 & Person2;

declare const staffer: Staff;

staffer.name;

// Generic Object Types

interface Box<Type> {
  contents: Type;
}

interface StringBox {
  contents: string;
}

let boxA: Box<string> = { contents: "hello" };
boxA.contents;

let boxB: StringBox = { contents: "world" };
boxB.contents;

type BoxType<Type> = {
  contents: Type;
}

type OrNull<Type> = Type | null;

type OneOrMany<Type> = Type | Type[];

type OneOrManyOrNull<Type> = OrNull<OneOrMany<Type>>;

type OneOrManyOrNullStrings = OneOrManyOrNull<string>;

// The Array type

// the ReadonlyArray type

const roArray: ReadonlyArray<string> = ["red", "blue", "green"];

// Tuple Types

type StringNumberPair = [string, number];

function doSomething(pair: [string, number]) {
  const a = pair[0];
  const b = pair[1];

  const [c, d] = pair;
}

doSomething(["hello", 42]);

type Either2dOr3d = [number, number, number?]

function setCoord(coord: Either2dOr3d) {
  const [_x, _y, _z] = coord;

  console.log(`Provided coordinate of length ${coord.length}`);
}

type StringNumberBooleans = [string, number, ...boolean[]];
type StringBooleansNumber = [string, ...boolean[], number];
type BooleansStringNumber = [...boolean[], string, number];

let point2 = [3, 4] as const;

//function distanceFromOrigin([x, y]: [number, number]) {
function distanceFromOrigin([x, y]: readonly [number, number]) {
  return Math.sqrt(x ** 2 + y ** 2);
}

distanceFromOrigin(point2);
