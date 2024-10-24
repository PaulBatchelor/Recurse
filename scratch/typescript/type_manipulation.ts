// vim:ts=2:sw=2:et

function identity<Type>(arg: Type): Type {
  return arg;
}

let output1 = identity<string>("hello world");
let output2 = identity("hello world");

// Working with Generic Type Variables

function loggingIdentity<Type>(arg: Array<Type>): Array<Type> {
  console.log(arg.length);
  return arg;
}

// Generic Types

let myIdentity: <Type>(arg: Type) => Type = identity;

let myIdentity2: { <Type>(arg: Type): Type } = identity;

interface GenericIdentityFn {
  <Type>(arg: Type): Type;
}

let myIdentity3: GenericIdentityFn = identity;

interface GenericIdentityFn2<Type> {
  (arg: Type): Type;
}

let myIdentity4: GenericIdentityFn2<number> = identity;

// Generic Classes

class GenericNumber<NumType> {
  zeroValue: NumType;
  add: (x: NumType, y: NumType) => NumType;
}

let myGenericNumber = new GenericNumber<number>();
myGenericNumber.zeroValue = 0;
myGenericNumber.add = function (x, y) {
  return x + y;
}

// Generic Constraints

interface lengthWise {
  length: number;
}

function loggingIdentity2<Type extends lengthWise>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}

//loggingIdentity2(3);
loggingIdentity2([3]);

// Using type parameters in Generic Constraints

function getProperty<Type, Key extends keyof Type>(obj: Type, key: Key) {
  return obj[key];
}

let x = { a: 1, b: 2, c: 3 };

let y = getProperty(x, 'a');
// let a = getProperty(x, 'm');

// Using Class Types in Generics

function create<Type>(c: { new(): Type }): Type {
  return new c();
}

class BeeKeeper {
  hasMask: boolean = true;
}

class ZooKeeper {
  nametag: string = "Mikle";
}

class Animal {
  numLegs: number = 4;
}

class Bee extends Animal {
  numLegs = 6;
  keeper: BeeKeeper = new BeeKeeper();
}

class Lion extends Animal {
  keeper: ZooKeeper = new ZooKeeper();
}

function createInstance<A extends Animal>(c: new () => A): A {
  return new c();
}

createInstance(Lion).keeper.nametag;
createInstance(Bee).keeper.hasMask;

// Generic Parameter Defaults

interface Container<_A, _B> {

}

// previously
declare function create1(): Container<HTMLDivElement, HTMLDivElement[]>;
declare function create1<T extends HTMLElement>(element: T): Container<T, T[]>;
declare function create1<T extends HTMLElement, U extends HTMLElement>(
  element: T,
  children: U[],
): Container<T, U[]>;


// using defaults to make optional generic parameters
declare function create2<T extends HTMLElement = HTMLDivElement, U extends HTMLElement[] = T[]>(
  element?: T,
  children?: U,
): Container<T, U>;

function foo<T = number, U = number>(a: T, b: U) {
  return [a, b];
}

let bar = foo<number, number>;
let bar2 = foo<number, string>;

let aa = bar(1, 2);

//let bb = bar(1, "2");
let bb = bar2(1, "2");

// Variance Annotations

interface Producer<T> {
  make(): T;
}

interface Consumer<T> {
  consume: (arg: T) => void;
}

interface Animal2 {

}

interface AnimalProducer {
  make(): Animal2;
}

interface Cat {

}

interface CatProducer {
  make(): Cat;
}


// Contravariant annotation
interface Consumer2<in T> {
  consume: (arg: T) => void;
}

// Covariant annotation

interface Producer2<out T> {
  make(): T;
}

// Invariant annotation

interface ProducerConsumer<in out T> {
  consume: (arg: T) => void;
  make(): T;
}

// keyof type operator

type Point = { x: number, y: number }
type P = keyof Point;

type Arrayish = { [n: number]: unknown }
type A = keyof Arrayish;

type Mapish = { [k: string]: unknown }

// M is string | number, object keys are always coerced to a string
type M = keyof Mapish;

// typeof operator
console.log(typeof "Hello world");
let s = "hello";
let n: typeof s;

type Predicate = (type: unknown) => boolean;
type K = ReturnType<Predicate>;

function f() {
  return { x: 10, y: 3 }
}

type P2 = ReturnType<typeof f>;

// Indexed access types

type Person = { age: number; name: string; alive: boolean }
type Age = Person["age"];

type I1 = Person["age" | "name"];

type I2 = Person [keyof Person];

type AliveOrName = "alive" | "name";
type I3 = Person[AliveOrName];

const MyArray = [
  {name: "Alice", age: 15},
  {name: "Alice", age: 15},
  {name: "Alice", age: 15},
];

type Person2 = typeof MyArray[number];
type Age2 = typeof MyArray[number]["age"];
type Age3 = Person["age"];

const key = "age";
type Age4 = Person[key];

// Conditional Types

interface Animal3 {
  live(): void;
}

interface Dog extends Animal3 {
  woof(): void;
}

type ex1 = Dog extends Animal ? number : string;
type ex2 = RegExp extends Animal ? number : string;

interface IdLabel {
  id: number;
}
interface NameLabel {
  name: string;
}

type NameOrId<T extends number | string> = T extends number
  ? IdLabel
  : NameLabel;

// can be used to simplify overloads to single function with no overloads

function createLabel<T extends number | string>(_idOrName: T): NameOrId<T> {
  throw "unimplmented";
}

let a = createLabel("typescript");
let b = createLabel(2.8);
let c = createLabel(Math.random() ? "hello" : 42);

// type MessageOf<T> = T["message"];

type MessageOf<T> = T extends { message: unknown } ? T["message"] : never;

interface Email {
  message: string;
}

interface EmailNumber {
  message: number;
}

interface Dog {
  bark(): void;
}

type EmailMessageContents = MessageOf<Email>;
type DogMessageContents = MessageOf<Dog>;
type EmailMessageContents2 = MessageOf<EmailNumber>;

type Flatten<T> = T extends any[] ? T[number] : T;

type c = Flatten<string []>;
type d = Flatten<number>;

// inferring within conditional types

// infer flatten implicitely instead of explicitely using indexed access type
type Flatten2<T> = T extends Array<infer Item> ? Item: T;

type GetReturnType<T> = T extends (...args: never[]) => infer Return ? Return : never;

type num = GetReturnType<() => number>;
type strfun = GetReturnType<(x: string) => string>s

// Distributive Conditional Types

type ToArray<T> = T extends any ? T[] : never;

type StrArrOrNumArr = ToArray<string | number>

// Mapped types

interface Horse {};

type OnlyBoolsAndHorses = {
  [key: string]:  boolean | Horse;
}

const conforms: OnlyBoolsAndHorses = {
  del: true,
  foo: false,
};

type OptionsFlag<Type> = {
  [Property in keyof Type]: boolean;
};