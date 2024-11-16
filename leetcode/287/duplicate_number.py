# 2024-11-16: found brute force quite easily, the O(n) O(1)
# solution I looked up O(1) space seems to really mean
# 1-2 variables, apparently. they don't scale with n, so
# maybe that's what it means?.
class Solution:
    # Floyd's Tortoise and Hare (Cycle Detection)
    def findDuplicate(self, nums: List[int]) -> int:
        tortoise = hare = nums[0]

        while True:
            tortoise = nums[tortoise]
            hare = nums[nums[hare]]
            if tortoise == hare:
                break

        tortoise = nums[0]
        while tortoise != hare:
            tortoise = nums[tortoise]
            hare = nums[hare]

        return hare

    # brute force
    def findDuplicate2(self, nums: List[int]) -> int:
        val = -1
        for i in range(len(nums)):
            val = nums[i]
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return nums[i]
        return -1
