from pprint import pprint

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

out = potions_and_spells([5, 1, 3], [1, 2, 3, 4, 5], 7)
assert(out == [4, 0, 3])
