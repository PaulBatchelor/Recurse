// Initial
let c=(b,l)=>WebAssembly.instantiate(new Int8Array(
[,97,115,109,1,,,,1,5,1,96,,1,127,3,2,1,,7,4,1,,,,10,
l=(b=b.split` `.flatMap(t=>t>-1?[65,t]:107+'-*/'.indexOf(t)))
.length+4,1,l-2,,...b,11]))

// And here's how to use it

(await c('11 11 1 - + 4 * 2 /')).instance.exports['']()

// Format it

let c1 = (b, l) =>
  WebAssembly.instantiate(
    new Int8Array([
      , 97, 115, 109, 1, , , , 1, 5, 1, 96, , 1, 127, 3, 2, 1, , 7, 4, 1, , , , 10,
      (l = (b = b.split` `.flatMap(
            (t) => t > -1 ? [65, t] : 107 + "-*/".indexOf(t)
           )).length + 4),
      1, l - 2, , ...b, 11
    ])
  );

// undo assignment expression

let c2 = (b, l) => {
  b = b.split` `.flatMap(
    (t) => (t > -1 ? [65, t] : 107 + "-*/".indexOf(t))
  );
  l = b.length + 4;
  return WebAssembly.instantiate(
    new Int8Array([
      , 97, 115, 109, 1, , , , 1, 5, 1, 96, , 1, 127, 3, 2, 1, , 7, 4, 1, , , ,
      10, l, 1, l - 2, , ...b, 11
    ]),
  );
};

/// Undo variable tricks

let c3 = (code) => {
  const instrs = code.split` `.flatMap(
    (t) => (t > -1 ? [65, t] : 107 + "-*/".indexOf(t))
  );
  const len = instrs.length + 4;
  return WebAssembly.instantiate(
    new Int8Array([
      , 97, 115, 109, 1, , , , 1, 5, 1, 96, , 1, 127, 3, 2, 1, , 7, 4, 1, , , ,
      10, len, 1, len - 2, , ...instrs, 11
    ]),
  );
};

// Add all zeros back

let c4 = (code) => {
  const instrs = code.split` `.flatMap(
    (t) => (t > -1 ? [65, t] : 107 + "-*/".indexOf(t))
  );
  const len = instrs.length + 4;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, len, 1, len - 2, 0, ...instrs, 11
    ]),
  );
};

// remove_4_bytes_len_definition

let c5 = (code) => {
  const instrs = code.split` `.flatMap(
    (t) => (t > -1 ? [65, t] : 107 + "-*/".indexOf(t))
  );
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// Write split as function call

let c6 = (code) => {
  const instrs = code.split(' ').flatMap(
    (t) => (t > -1 ? [65, t] : 107 + "-*/".indexOf(t))
  );
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// write ternary as if statement

let c7 = (code) => {
  const instrs = code.split(" ").flatMap((t) => {
    if (t > -1) {
      return [65, t];
    } else {
      return 107 + "-*/".indexOf(t);
    }
  });
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// remove number check with coercion

let c8 = (code) => {
  const instrs = code.split(" ").flatMap((t) => {
    const num = parseInt(t, 10);
    if (Number.isFinite(num)) {
      return [65, num];
    } else {
      return 107 + "-*/".indexOf(t);
    }
  });
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// undo minus-one trick

let c9 = (code) => {
  const instrs = code.split(" ").flatMap((t) => {
    const num = parseInt(t, 10);
    if (Number.isFinite(num)) {
      return [65, num];
    } else {
      return 106 + "+-*/".indexOf(t);
    }
  });
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// remove indexOf trick completely

const OP_TO_BYTECODE = {
  "+": 106,
  "-": 107,
  "*": 108,
  "/": 109,
};

let c10 = (code) => {
  const instrs = code.split(" ").flatMap((t) => {
    const num = parseInt(t, 10);
    if (Number.isFinite(num)) {
      return [65, num];
    } else {
      return OP_TO_BYTECODE[t] ?? 106;
    }
  });
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 4, 1, 0, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// name exported function as 'a'

const OP_TO_BYTECODE = {
  "+": 106,
  "-": 107,
  "*": 108,
  "/": 109,
};

let c11 = (code) => {
  const instrs = code.split(" ").flatMap((t) => {
    const num = parseInt(t, 10);
    if (Number.isFinite(num)) {
      return [65, num];
    } else {
      return OP_TO_BYTECODE[t] ?? 106;
    }
  });
  const len = instrs.length;
  return WebAssembly.instantiate(
    new Int8Array([
      0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 5, 1, 1, 97, 0, 0,
      10, 4 + len, 1, 2 + len, 0, ...instrs, 11
    ]),
  );
};

// Bytes in array
    [
      // Wasm module magic number '\0asm'
      [0, 97, 115, 109],
      // Wasm version 1.0
      [1, 0, 0, 0],

      // ----- type section -----

      1, // Section identifier
      5, // Section size in bytes

      1, // Number of entries that follow

      // type section - entry 0
      96, // Type `function`
      0,  // Number of parameters
      1,  // Number of return values

      127, // return type i32

      // ----- function section -----

      3, // Section identifier
      2, // Section size in bytes
      1, // Number of entries that follow

      // function section - entry 0
      0, // Index of the type section entry

      // ----- export section -----

      7, // Section identifier
      5, // Section size in bytes
      1, // Number of entries that follow

      // export section - entry 0
      1,  // Name size in bytes
      97, // String as utf-8 bytes for 'a'
      0,  // Export type `function`
      0,  // Function Index

      // ----- code section -----

      10, // Section identifier
      4 + len, // Section size in bytes

      1, // Number of entries that follow

      // code section - entry 0
      2 + len, // Entry size in bytes
      0, // Number of local variables
      ...instrs,
      11, // `end` instruction
    ]
