# 2024-12-31: following explore card

class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        dp = [0] * len(nums)

        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
        return dp[-1]
    # top-down
    def rob_topdown(self, nums: List[int]) -> int:
        def dp(i):
            if i == 0:
                return nums[i]
            if i == 1:
                return max(nums[1], nums[0])

            if i not in memo:
                memo[i] = max(nums[i] + dp(i - 2), dp(i - 1))
            return memo[i]

        memo = {}

        return dp(len(nums) - 1)


# 2024-11-12 This one actually works. My previous attempt
# I did a few months ago doesn't pass all the edge cases.
# Approach: start with recursive approach, then add
# caching/memoization. The recursive function encapsulates
# the recurrance relation

class Solution:
    def rob_r(self, nums: List[int], pos: int)->int:
        if pos >= len(nums):
            return 0
        if self.cache[pos] >= 0:
            return self.cache[pos]
        v1 = nums[pos] + self.rob_r(nums, pos + 2)
        v2 = 0
        if (pos + 1) < len(nums):
            v2 = nums[pos + 1] + self.rob_r(nums, pos + 3)
        self.cache[pos] = max(v1, v2)
        return self.cache[pos]
    def rob(self, nums: List[int]) -> int:
        self.cache = [-1]*len(nums)
        return self.rob_r(nums, 0)
