// vim:ts=2:sw=2:et

// function type expressions
function greeter(fn: (a: string) => void) {
  fn("Hello, world!");
}

function printToConsole(s: string) {
  console.log(s);
}

greeter(printToConsole);

type GreetFunction = (a: string) => void;

function greeter2(fn: GreetFunction) {
  fn("Hello, world!");
}

greeter2(printToConsole);

// call signatures

type DescribableFunction = {
  description: string;
  (someArg: number): boolean;
}

function doSomething(fn: DescribableFunction) {
  console.log(fn.description + " returned " + fn(6));
}

function myFunc(someArg: number) {
  return someArg > 3;
}

myFunc.description = "default description";

doSomething(myFunc);

// Construct Signatures

type SomeConstructor = {
  new(s: string): Shape;
}

function fn(ctor: SomeConstructor) {
  return new ctor("hello");
}

interface CallOrConstruct {
  (n?: number): string;
  new(s: string): Date;
}

function fn2(ctor: CallOrConstruct) {
  console.log(ctor(10));
  console.log(new ctor("10"));
}

// generic functions

function firstElem0(arr: any[]) {
  return arr[0];
}

function firstElem<Type>(arr: Type[]): Type | undefined {
  return arr[0];
}

const s2 = firstElem(["a", "b", "c"]);
const s3 = firstElem([1, 2, 3]);
const u = firstElem([]);

function map<Input, Output>(arr: Input[], func: (arg: Input) => Output): Output[] {
  return arr.map(func);
}

const parsed = map(["1", "2", "3"], (n) => parseInt(n));

// constraints

function longest<Type extends { length: number }>(a: Type, b: Type) {
  if (a.length >= b.length) {
    return a;
  } else {
    return b;
  }
}

const longerArray = longest([1, 2], [1, 2, 3]);
const longerString = longest("hello", "world!");
// const notOk = longest(10, 100);

// function minimumLength<Type extends { length: number }>(
//   obj: Type,
//   minimum: number,
// ): Type {
//   if (obj.length >= minimum) {
//     return obj;
//   } else {
//     return { length: minimum }
//   }
// }

// Specifying Type Arguments

function combine<Type>(arr1: Type[], arr2: Type[]): Type[] {
  return arr1.concat(arr2);
}

// const arr = combine([1, 2, 3], ["hello"]);
const arr = combine<string | number>([1, 2, 3], ["hello"]);

// guidelines for writing good generic functions

function firstElement1<Type>(arr: Type[]) {
  return arr[0];
}

function firstElement2<Type extends any[]>(arr: Type) {
  return arr[0];
}

const a1 = firstElement1([1, 2, 3]);
const b1 = firstElement2([1, 2, 3]);

function filter1<Type>(arr: Type[], func: (arg: Type) => Boolean): Type[] {
  return arr.filter(func);
}

function filter2<Type, Func extends (arg: Type) => Boolean>(
  arr: Type[],
  func: Func
) {
  return arr.filter(func);
}

function greet1<Str extends string>(str: Str) {
  console.log("Hello " + str);
}

function greet2(str: string) {
  console.log("Hello " + str);
}

// Optional Parameters
// Optional Parameters in Callbacks

function myForEach(arr: any[], callback: (arg: any, index?: number) => void) {
  for (let i = 0; i < arr.length; i++) {
    callback(arr[i], i);
  }
}

// myForEach([1, 2, 3], (_a, i) => console.log(i.toFixed());

// Function Overloads

function makeDate(timestamp: number): Date;
function makeDate(m: number, d: number, y: number): Date;
function makeDate(mOrTimeStamp: number, d?: number, y?: number): Date {
  if (d !== undefined && y !== undefined) {
    return new Date(y, mOrTimeStamp, d);
  } else {
    return new Date(mOrTimeStamp);
  }
}

const d1 = makeDate(12345678);
const d2 = makeDate(5, 5, 5);
// const d3 = makeDate(1, 3);

// Overload signatures and the implementation signature

// Writing good overloads


function len(s: string): number;
function len(arr: any[]): number;
function len(x: any) {
  return x.length;
}

len("");
len([0]);
// len(Math.random() > 0.5 ? "hello" : [0]);

// Declaring =this= in a function

const user4 = {
  id: 123,
  admin: false,

  becomeAdmin: function () {
    this.admin = true;
  }
}

interface DB {
  filterUsers(filter: (this: User) => boolean): User[];
}

// Other types to know about

// in typescript, void is not the same thing as undefined

function noop() {
  return;
}

function f1(a: any) {
  return a.b();
}

// function f2(a: unknown) {
//   return a.b();
// }


function safeParse(s: string): unknown {
  return JSON.parse(s);
}

const json_obj = safeParse("{}");

function fail(msg: string): never {
  throw new Error(msg);
}

function fn3(x: string | number) {
  if (typeof x === "string") {

  } else if (typeof x === "number") {

  } else {
    x;
  }
}

// rest parameters and arguments

function multiply(n: number, ...m: number[]) {
  return m.map((x) => n * x);
}

const a2 = multiply(10, 1, 2, 3, 4);

const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

arr1.push(...arr2);

//const args = [8, 5];
const args = [8, 5] as const;
const angle = Math.atan2(...args);

// Parameter Destructuring

function sum({ a, b, c }: { a: number, b: number, c: number }) {
  console.log(a + b + c);
}

sum({ a: 10, b: 20, c: 30 });

type ABC = { a: number; b: number; c: number };

function sum2({ a, b, c }: ABC) {
  console.log(a + b + c);
}

// Assignability of Functions

type voidFunc = () => void;

const vf1: voidFunc = () => {
  return true;
};

const vf2: voidFunc = () => true;

const vf3: voidFunc = function () {
  return true;
};

// function vf4(): void {
//   return true;
// }
