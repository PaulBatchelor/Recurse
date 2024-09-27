# 3sum: this feels like a backtracking problem. How to
# avoid O(n^3) time? Sorting the list might do something.
from pprint import pprint

def approach1(nums):
    N = len(nums)
    out = []

    # to make backtracking work
    # make sure i < j < k
    # make sure nums[i] <= nums[j] <= nums[k]

    # sort the list to make sure ordering holds
    nums = sorted(nums)

    # set of target k values -(nums[i] + nums[j])
    h = set()

    # fundamentally, this is more or less written
    # as a bruteforce loop with lots of escape hatches
    # I don't love the nested loops
    for i in range(0, N):
        for j in range(1, N):
            if i >= j:
                continue
            target = -(nums[j] + nums[i])
            if target in h:
                continue
            h.add(target)
            for k in range(2, N):
                if j >= k:
                    continue
                if nums[k] == target:
                    out.append([nums[i], nums[j], nums[k]])
                    continue
    return out

# transcribed from pseudo-code in wikipedia,
# modified with set for uniqueness combinations
def twopointer(nums):
    nums = sorted(nums)
    N = len(nums)
    out = []
    h = set()

    for i in range(0, N - 2):
        a = nums[i]
        start = i + 1
        end = N - 1

        while (start < end):
            b = nums[start]
            c = nums[end]
            if (a + b + c) == 0:
                target = -(a + b)
                if target not in h:
                    out.append([a, b, c])
                h.add(target)
                start += 1
                end -= 1
            elif (a + b + c) > 0:
                end -= 1
            else:
                start += 1

    return out

def flatten(triplets):
    out = []

    for row in triplets:
        out.extend(row)
    return sorted(out)

def test(f):
    nums = [-1, 0, 1, 2, -1, 4]
    expected = flatten([[-1, -1, 2], [-1, 0, 1]])
    output = flatten(f(nums))
    assert(expected == output)

    nums = [0, 1, 1]
    expected = []
    output = f(nums)
    assert(expected == output)

test(approach1)
test(twopointer)
