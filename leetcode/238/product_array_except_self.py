# The problem specifically said not to use division, and
# to make it O(n) time. Nothing about space constraints.
# What I worked out on paper was to try to use a kind
# of "prefix product" list (like prefix sums, but with
# products). Two lists, one going left to right, then
# the other going right to left. The idea being that the
# product of those two lists end up being the total product
# minus one. Populating the tables takes linear time, but
# O(2n) is still O(n).

from pprint import pprint

def prod_minus_self(x):
    out = []
    N = len(x)
    pleft = [1]*N
    pright = [1]*N

    pleft[0] = 1
    pright[N - 1] = 1

    for i in range(1, N):
        pleft[i] = pleft[i - 1] * x[i - 1]
        pright[N - i - 1]  = pright[N - i] * x[N - i]

    for i in range(0, N):
        out.append(pleft[i] * pright[i])

    return out

# WIP: do this the way you'd expect by getting
# total product and dividing by current item
# use repeated subtracted instead of division
def prod_minus_self_constant(x):
    total = 1
    out = []
    for val in x:
        total *= val

    for i in range(0, len(x)):
        ans = 0
        amt = total
        while amt > 0:
            ans += 1
            amt -= x[i]
        out.append(ans)

    pprint(out)
    return out

def test(f):
    out = f([1, 2, 3, 4])
    assert(out == [24, 12, 8, 6])

    out = f([-1, 1, 0, -3, 3])
    assert(out == [0, 0, 9, 0, 0])

test(prod_minus_self)

# Work in progress
# test(prod_minus_self_constant)
