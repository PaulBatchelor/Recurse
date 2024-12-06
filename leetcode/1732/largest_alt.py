# 2024-12-6
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        largest = 0
        alt = 0
        for i in range(len(gain)):
            alt += gain[i]
            largest = max(largest, alt)

        return largest
