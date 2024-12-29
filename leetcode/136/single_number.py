# 2024-12-28: suddenly, this clicked for me
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        out = 0
        for n in nums:
            out ^= n
        return out
