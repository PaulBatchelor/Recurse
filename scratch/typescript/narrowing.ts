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

function move(animal: Fish | Bird) {
    if ("swim" in animal) {
        return animal.swim();
    }
    return animal.fly();
}
