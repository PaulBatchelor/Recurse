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
