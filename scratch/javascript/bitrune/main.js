function mkCheckBox() {
    let div = document.createElement("div");
    div.className="checkbox";
    let input = document.createElement("input");
    input.type = "checkbox";
    div.appendChild(input);
    return div;
}

function mkGrid(nrows, ncols) {
    let div = document.createElement("div");
    div.className ="grid";
    for (let i = 0; i < nrows*ncols; i++) {
        let cb = mkCheckBox()
        div.appendChild(cb)
    }
    let container = document.createElement("div");
    container.appendChild(div);
    container.className="container";
    return container;
}

console.log("hello");
let body = document.getElementsByTagName("body").item(0);
let p = document.createElement("p");
p.appendChild(document.createTextNode("hello world"));
body.appendChild(p);
body.appendChild(mkGrid(3, 3));