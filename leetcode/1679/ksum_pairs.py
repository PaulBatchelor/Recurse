# 2024-12-04 Interesting, my previous approach used a
# hashmap rather than the two-pointer and sorted list
# approach.

class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        nums = sorted(nums)
        left = 0
        right = len(nums) - 1
        npairs = 0

        while left < right:
            lrsum = nums[left] + nums[right]

            # remove both
            if lrsum == k:
                left += 1
                right -= 1
                npairs += 1
            elif lrsum < k:
                left += 1
            else:
                right -= 1
        return npairs
