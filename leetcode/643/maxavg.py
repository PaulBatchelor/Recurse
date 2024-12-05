# 2024-12-04 My solution plus the editorial cumulative sum
class Solution:
    # cumulative sum version from editorial
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        csum = [0]*len(nums)
        csum[0] = nums[0]

        for i in range(1, len(nums)):
            csum[i] = csum[i - 1] + nums[i]

        maxsum = csum[k - 1]
        for i in range(k, len(nums)):
            maxsum = max(csum[i] - csum[i - k], maxsum)

        return maxsum / k
    # my version, sliding window
    def findMaxAverageV1(self, nums: List[int], k: int) -> float:
        window = 0

        # our initial sum
        for i in range(k):
            window += nums[i]

        maxsum = window
        # sliding window, subtract from left, add on right
        for i in range(k, len(nums)):
            # subtract leftmost value
            # window -= nums[i - k]
            # # add current value
            # # TODO we could be fancy and consolidate
            # window += nums[i]
            window += nums[i] - nums[i - k]
            maxsum = max(window, maxsum)

        return maxsum / k



