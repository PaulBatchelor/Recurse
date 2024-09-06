# Max number of k-sum pairs
# Implementing the various approaches for solving this one.
# The LC75 has it in the "two-pointer" category, though
# the more intuitive approaches use a double and single-pass
# hashmap.

from pprint import pprint

# 2 pass: build the hashmap, then remove elements from it
# to find complement
def ksum_hash_2pass(nums, k):
    hmap = {}
    npairs = 0

    for i in nums:
        if i in hmap:
            hmap[i] += 1
        else:
            hmap[i] = 1

    for i in nums:
        # make sure that it's still in the hashmap,
        # as it could have been removed
        if i in hmap:
            comp = k - i
            hmap[i] -= 1
            # every element we sweep through gets peeled
            # off first. This is to prevent duplicates
            if hmap[i] <= 0: hmap.pop(i)

            # check to see if complement value exists
            if comp in hmap:
                hmap[comp] -= 1
                npairs += 1
                if hmap[comp] <= 0:
                    hmap.pop(comp)

    return npairs

# 1 pass optimizes from 2-pass. Build the hashmap as you
# go instead of having it be one step
def ksum_hash_1pass(nums, k):
    hmap = {}
    npairs = 0
    for i in nums:
        comp = k - i
        if comp in hmap:
            hmap[comp] -= 1
            if hmap[comp] <= 0:
                hmap.pop(comp)
            npairs += 1
        else:
            if i in hmap:
                hmap[i] += 1
            else:
                hmap[i] = 1

    return npairs

# two-pointer: this approach sorts the array and uses
# two pointers to find matching pairs.

def ksum_2pointer(nums, k):
    npairs = 0
    nums.sort(reverse=True)
    left = 0
    right = len(nums) - 1

    while left < right:
        s = nums[left] + nums[right]
        if s < k:
            right -= 1
        elif s > k:
            left += 1
        else:
            npairs += 1
            left += 1
            right -= 1

    return npairs

def test_ksum(f):
    out = f([1, 2, 3, 4], 5)
    assert(out == 2)
    out = f([3, 1, 3, 4, 3], 6)
    assert(out == 1)

test_ksum(ksum_hash_2pass)
test_ksum(ksum_hash_1pass)
test_ksum(ksum_2pointer)
