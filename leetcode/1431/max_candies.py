# 2024-11-28 Huh. I guess that was it.
class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        maxCandies = max(candies)
        return [(c + extraCandies) >= maxCandies for c in candies]
