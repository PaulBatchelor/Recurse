def trib(n):
    t0 = 0
    t1 = 1
    t2 = 1

    if n == 0: return t0
    if n == 1: return t2
    if n == 2: return t3

    for i in range(3, n):
        t3 = t0 + t1 + t2
        t0 = t1
        t1 = t2
        t2 = t3

    return t0 + t1 + t2

out = trib(4)
assert(out == 4)

out = trib(25)
assert(out == 1389537)
