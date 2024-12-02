# 2024-12-02: two-pointer got me thinking left/right,
# but tripped up on edge cases

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        left = 0
        right = 0
        while right < len(nums):
            if nums[left] != 0:
                left += 1
                right = left + 1
                continue
            if nums[right] == 0:
                right += 1
                continue
            nums[left], nums[right] = nums[right], nums[left]




# 0 1 0 3 12
# 1 0 0 3 12
# 1 3 0 0 12
# 1 3 12 0 0
