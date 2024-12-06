# 2024-12-06: My in-memory prefix sum cumulative sum worked
# and I reached it pretty quickly. However, what I didn't
# see was that the solution where you could get the
# right sum from a growing leftsum and the total sum
class Solution:
    # editorial
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        leftsum = 0
        for i in range(len(nums)):
            if leftsum == (total - leftsum - nums[i]):
                return i
            leftsum += nums[i]

        return -1

    def pivotIndexV1(self, nums: List[int]) -> int:
        psum = []
        for i in range(len(nums)):
            if i == 0:
                psum.append(nums[i])
            else:
                psum.append(nums[i] + psum[i - 1])

        for i in range(len(nums)):
            lsum = rsum = 0
            if i > 0:
                lsum = psum[i - 1]
            rsum = psum[len(nums) - 1] - psum[i]
            if rsum == lsum:
                return i
        return -1
