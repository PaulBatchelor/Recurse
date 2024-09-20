def twosum(x, target):
    h = {}

    for i in range(0, len(x)):
        pair = target - x[i]
        if pair in h:
            return [h[pair], i]
        else:
            h[x[i]] = i

    return [None, None]

out = twosum([2, 7, 11, 15], 9)
assert(out == [0, 1] or out == [1, 0])

out = twosum([3, 2, 4], 6)
assert(out == [1, 2] or out == [2, 1])

out = twosum([3, 3], 6)
assert(out == [0, 1] or out == [1, 0])
