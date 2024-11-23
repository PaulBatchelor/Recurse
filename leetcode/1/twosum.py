# 2024-11-23: answer whipped up. I wanted a structure
# that had only one return
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pair = []
        # hashmap dictionary
        hm = {}

        # iterate through indices 0 .. N -1
        for i in range(len(nums)):
            x = nums[i]
            # is current number a match for a previously found number?
            if x in hm:
                pair = [hm[x], i]
                break
            ideal = target - x
            # our ideal value points to the indices
            # of the previous value
            hm[ideal] = i

        return pair

# old version
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
