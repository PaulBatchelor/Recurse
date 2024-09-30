# I couldn't resist doing this one

def op_add(stk):
    a = stk.pop()
    b = stk.pop()
    stk.append(a + b)

def op_div(stk):
    b = stk.pop()
    a = stk.pop()
    stk.append(a // b)

def op_sub(stk):
    b = stk.pop()
    a = stk.pop()
    stk.append(a - b)

def op_mul(stk):
    b = (stk.pop())
    a = stk.pop()
    stk.append(a * b)

def rpn(tokens):
    stk = []
    ops = {
        "+": op_add,
        "/": op_div,
        "-": op_sub,
        "*": op_mul
    }
    for t in tokens:
        if t.isnumeric():
            stk.append(int(t))
        elif t in ops:
            ops[t](stk)
    return stk.pop()

tk = "2 1 + 3 *".split(' ')
rc = rpn(tk)
assert(rc == 9)

tk = "4 13 5 / +".split(' ')
rc = rpn(tk)
assert(rc == 6)
