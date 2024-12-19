# 2024-12-19: this is mine, which closely resembles the
# editorial. Getting the conditional right for binary
# search was trial and error for me here. I wish I had
# better intuition for this.

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left = 1
        right = max(piles)

        while left < right:
            mid = left + (right - left) // 2
            nhours = 0
            for bananas in piles:
                nhours += ceil(bananas / mid)

            if nhours <= h:
                right = mid
            else:
                left = mid + 1

        return left
