from pprint import pprint

def counting_bits(n):
    a = [0]*(n + 1)
    pos = 0

    # make it go n + 1 times
    c = n << 1

    while (c):
        for i in range(0, n + 1):
            if i & (1 << pos):
                a[i] += 1
        c >>= 1
        pos += 1
    return a

out = counting_bits(2)
assert(out == [0, 1, 1])

out = counting_bits(5)
assert(out == [0, 1, 1, 2, 1, 2])
