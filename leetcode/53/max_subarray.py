# 2024-11-17: So, I didn't actually solve this problem
# correctly the first time. Like before, I tried to shove
# it into a two-pointer solution in an attempt to whittle
# things down to an ideal window. Kadane's algorithm
# turns out to be the best. I also included the brute force
# solution, which I didn't come up with either.

class Solution:
    # kadane's algorithm
    def maxSubArray(self, nums: List[int]) -> int:
        best_sum = -inf
        cur_sum = 0
        for x in nums:
            cur_sum = max(x, cur_sum + x)
            best_sum = max(cur_sum, best_sum)
        return best_sum
    # brute force
    def maxSubArrayBrute(self, nums: List[int]) -> int:
        max_subarray = -math.inf

        for i in range(len(nums)):
            current_subarray = 0
            for j in range(i, len(nums)):
                current_subarray += nums[j]
                max_subarray = max(max_subarray, current_subarray)

        return max_subarray
