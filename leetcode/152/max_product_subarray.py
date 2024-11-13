# 2024-11-13 After brute-forcing, and attempting two-pointer,
# I looked up the answer using dynamic programming

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        min_so_far = nums[0]
        max_so_far = nums[0]
        res = max_so_far
        for x in nums[1:]:
            tmp = max(x, max(max_so_far*x, min_so_far*x))
            min_so_far = min(x, min(min_so_far*x, max_so_far*x))
            max_so_far = tmp
            res = max(res, max_so_far)
        return res
