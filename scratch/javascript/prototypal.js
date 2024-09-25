// vim:ts=4:sw=4:et

function Animal(name) {
    this.name = name;
}

Animal.prototype.makeSound = function () {
    console.log('The ' + this.constructor.name + ' makes a sound');
}

function Dog(name) {
    Animal.call(this, name);
}

Object.setPrototypeOf(Dog.prototype, Animal.prototype);

Dog.prototype.bark = function () {
    console.log("woof!");
}

const bolt = new Dog('bolt');

console.log(bolt.name);

bolt.makeSound()
bolt.bark();
