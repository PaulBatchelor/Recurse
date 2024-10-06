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
// TBD.
