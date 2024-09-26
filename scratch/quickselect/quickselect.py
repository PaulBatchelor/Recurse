# https://en.wikipedia.org/wiki/Quickselect
from pprint import pprint
from random import randrange, seed, shuffle

def partition(list, left, right, pivot_idx):
    pivot_val = list[pivot_idx]
    list[pivot_idx], list[right] = list[right], list[pivot_idx]
    store_idx = left

    for i in range(left, right):
        if list[i] < pivot_val:
            list[store_idx], list[i] = list[i], list[store_idx]
            store_idx += 1

    list[right], list[store_idx] = list[store_idx], list[right]
    return store_idx

def select(list, left, right, k):
    if left == right:
        return list[left]
    pivot_idx = left + randrange(right - left + 1)
    pivot_idx = partition(list, left, right, pivot_idx)

    if k == pivot_idx:
        return list[k]
    elif k < pivot_idx:
        return select(list, left, pivot_idx - 1, k)
    else:
        return select(list, pivot_idx + 1, right, k)


list = [0, 2, 4, 8, 5]
expected = []
seed()
for i in range(0, len(list)):
    x = select(list, 0, len(list) - 1, i)
    expected.append(x)

shuffle(list)
for i in range(0, len(list)):
    y = select(list, 0, len(list) - 1, i)
    assert(y == expected[i])
