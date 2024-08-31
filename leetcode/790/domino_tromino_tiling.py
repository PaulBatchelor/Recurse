# spent a great deal of time trying to derive this
# let's see if it works

def domtrom(n):
    # figure out these combinations in advance
    # the first 3 n values
    c0 = 1
    c1 = 2
    c2 = 5

    c = [0]*4

    c[0] = 1
    c[1] = 2
    c[2] = 5

    if n < 4:
        return c[n - 1]

    for i in range(3, n):
        # c0 is used twice because there are two prefixes
        # that have length 3
        c[3] = c[2] + c[1] + 2*c[0]
        
        # update state
        c[0] = c[1]
        c[1] = c[2]
        c[2] = c[3]

    return c[3]

out = domtrom(3)
assert(out == 5)
out = domtrom(4)
assert(out == 9)
