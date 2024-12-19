# 2024-12-19: My left/right dyslexia is going to get me.
# I was handling the return value backwards. This is kind
# of reminding my of daylight savings time logic. Like,
# what does it mean to set the clock back? I need a few
# moments to work it out.
class Solution:
    def guessNumber(self, n: int) -> int:
        left = 1
        right = n
        while left < right:
            mid = left + (right - left)//2
            res = guess(mid)
            if res < 0:
                right = mid - 1
            elif res > 0:
                left = mid + 1
            else:
                return mid
        return left
