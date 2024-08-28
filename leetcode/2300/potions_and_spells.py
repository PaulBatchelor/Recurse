from pprint import pprint
import bisect
import math

def potions_and_spells(spells, potions, success):
    potions.sort()
    m = len(potions)
    n = len(spells)
    results = []

    for i in range(0, n):
        high = m
        low = 0
        s = spells[i]
        found = -1

        if s * potions[m - 1] < success:
            results.append(0)
            continue

        while low <= high and low >= 0:
            mid = low + (high - low)//2
            r1 = s * potions[mid]
            r2 = s * potions[mid + 1]

            if r1 < success and r2 >= success:
                found = mid
                break
            elif r1 >= success and r2 >= success:
                high = mid - 1
            else:
                low = mid + 1
            
        results.append(m - (found + 1))


    return results

# editorial version is a little fancier for binary
# search, making use of built-in functions
def potions_and_spells_v2(spells, potions, success):
    potions.sort()
    results = []
    max_potion = potions[-1]
    m = len(potions)
    for s in spells:
        min_potion = math.ceil(success / s)
        if min_potion > max_potion:
            results.append(0)
        else:
            idx = bisect.bisect_left(potions, min_potion)
            results.append(m - idx)

    return results

out = potions_and_spells([5, 1, 3], [1, 2, 3, 4, 5], 7)
assert(out == [4, 0, 3])

out = potions_and_spells_v2([5, 1, 3], [1, 2, 3, 4, 5], 7)
assert(out == [4, 0, 3])
