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
