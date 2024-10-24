# 2024-10-24 Small enough to use recursion
from copy import deepcopy
class Solution:
    def subsets_r(self, nums: List[int], start: int, combo: List[int], out: List[int]):
        # iterate from starting index to end

        for i in range(start, len(nums)):
            combo.append(nums[i])
            out.append(deepcopy(combo))
            self.subsets_r(nums, i + 1, combo, out)
            combo.pop()

    def subsets(self, nums: List[int]) -> List[List[int]]:
        out = [[]]
        combo = []
        self.subsets_r(nums, 0, combo, out)
        return out
