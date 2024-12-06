# 2024-12-06: after grokking the sliding pattern from LC1004,
# this one was reasonaby straightforward.
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        left = 0
        nzeros = 0
        for right in range(len(nums)):
            nzeros += int(nums[right] == 0)
            if nzeros > 1:
                nzeros -= int(nums[left] == 0)
                left += 1

        return right - left
