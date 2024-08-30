# implementing various versions of the cut rod example from
# the CLRS algorithms book

# recursive top-down (pg 363)
def cut_rod(p, n):
    if n == 0:
        return 0

    q = -1
    for i in range(1, n + 1):
        q = max(q, p[i] + cut_rod(p, n - i))

    return q

# memoized rod cut (pg 365)

def memoized_cut_rod_aux(p, n, r):
    q = -1
    if r[n] >= 0:
        return r[n]

    if n == 0:
        q = 0
    else:
        for i in range(1, n + 1):
            q = max(q, p[i] + memoized_cut_rod_aux(p, n - i, r))
    r[n] = q

    return q

def memoized_cut_rod(p, n):
    r = [0]*(n+1)
    for i in range(0, n + 1):
        r[i] = -1

    return memoized_cut_rod_aux(p, n, r)


def bottom_up_cut_rod(p, n):
    r = [0]*(n + 1)
    r[0] = 0

    for j in range(1, n + 1):
        q = -1
        for i in range(1, j + 1):
            q = max(q, p[i] + r[j - i])
        r[j] = q

    return r[n]

p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
out = cut_rod(p, 4)
assert(out == 10)

out = memoized_cut_rod(p, 4)
assert(out == 10)

out = bottom_up_cut_rod(p, 4)
assert(out == 10)

