// vim:ts=4:sw=4:et

function padLeft(padding: number | string, input: string): string {
    if (typeof padding === "number") {
        return " ".repeat(padding) + input;
    }

    return padding + input;
}

function printAll(strs: string | string[] | null) {
    if (strs && typeof strs === "object") {
        for (const s of strs) {
            console.log(s);
        }
    } else if (typeof strs === "string") {
        console.log(strs);
    } else {

    }
}

function getUsersOnlineMessage(numUsersOnline: number): string {
    // coercion
    if (numUsersOnline) {
        return `There are ${numUsersOnline} people online`;
    }
    return "Nobody's here :(";
}

function printAllv2(strs: string | string[] | null) {
    if (strs !== null) {
        if (typeof strs === "object") {
            for (const s in strs) {
                console.log(s)
            }
        } else if (typeof strs === "string") {
            console.log(strs)
        }
    }
}

interface Container {
    value: number | null | undefined;
}

// the looser != (as opposed to !==) checks for both null and undefined
function multiplyValue(container: Container, factor: number) {
    if (container.value != null) {
        console.log(container.value);
        container.value *= factor;
    }
}

// in operator narrowing

type Fish = { swim: () => void };
type Bird = { fly: () => void };
type Human = { swim?: () => void; fly?: () => void; }

function move(animal: Fish | Bird) {
    if ("swim" in animal) {
        return animal.swim();
    }
    return animal.fly();
}

function move2(animal: Fish | Bird | Human) {
    if ("swim" in animal) {
        animal;
    } else {
        animal;
    }

}

// instanceof narrowing

function logValue(x: Date | string) {
    if (x instanceof Date) {
        console.log(x.toUTCString());
    } else {
        console.log(x.toUpperCase());
    }
}

// assigments
{
    let x = Math.random() < 0.5 ? 1.0 : "hello world!";

    x = 1;

    console.log(x);

    x = "goodbye";

    console.log(x);

    // doesn't work: declared type doesn't have boolean
    // x = true;
}

// control flow analysis

// using type predicates

function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}

// discriminated unions

interface Shape {
    kind: "circle" | "square";
    radius?: number;
    sideLength?: number;
}

function getArea(shape: Shape) {
    if (shape.kind == "circle") {
        return Math.PI * shape.radius! ** 2;
    }

}

interface Circle {
    kind: "circle";
    radius: number;
}

interface Square {
    kind: "square";
    sideLength: number;
}

type Shape2 = Circle | Square;

function getArea2(shape: Shape2) {
    if (shape.kind == "circle") {
        return Math.PI * shape.radius ** 2;
    }
}

function getArea3(shape: Shape2) {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "square":
            return shape.sideLength ** 2;
    }
}

// Exhaustiveness checking

interface Triangle {
    kind: "triangle";
    sideLength: number;
}

type Shape3 = Shape2;
//type Shape3 = Shape2 | Triangle;

function getArea4(shape: Shape3) {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "square":
            return shape.sideLength ** 2;
        default:
            const _exhaustiveCheck: never = shape;
            return _exhaustiveCheck;
    }
}
