from pprint import pprint
def minmoststairs(costs):
    c = [0] * (len(costs) + 1)

    for n in range(2, len(costs) + 1):
        c[n] = min(c[n - 2] + costs[n - 2], c[n - 1] + costs[n - 1])

    return c[-1]

out = minmoststairs([10, 15, 20])
assert(out == 15)

out = minmoststairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1])
assert(out == 6)
