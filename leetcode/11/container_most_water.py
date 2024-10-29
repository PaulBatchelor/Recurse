# 2024-10-28: I've done this one too many times...

class Solution:
    def maxArea(self, height: List[int]) -> int:
        out = 0
        left = 0
        right = len(height) - 1

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            out = max(out, area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return out
