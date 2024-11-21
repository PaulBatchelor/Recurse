# 2024-11-21: The optimized solution is fairly disappointing
# "clever", but ultimately the same approach
class Solution:
    # The "clever" solution
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        out = [1] * n

        for i in range(1, n):
            out[i] = out[i - 1] * nums[i - 1]

        R = 1
        for i in reversed(range(n)):
            out[i] *= R
            R *= nums[i]

        return out

    # left/right product lists
    def productExceptSelfV1(self, nums: List[int]) -> List[int]:
        n = len(nums)
        left = [1]*n
        right = [1]*n
        out = []

        for i in range(n):
            if i > 0:
                left[i] = left[i - 1] * nums[i - 1]
                right[n - i - 1] = right[n - i] * nums[n - i]

        for i in range(n):
            out.append(left[i] * right[i])
        return out
    def productExceptSelf_bruteforce(self, nums: List[int]) -> List[int]:
        out = []
        n = len(nums)

        for i in range(n):
            prod = 1
            for j in range(n):
                if j == i:
                    continue
                prod *= nums[j]
            out.append(prod)
        return out

