# 2024-10-21
# solved with dynamic programming via memoization
# it was helpful to know the upper limit
class Solution:
    def __init__(self):
        self.cache = [None]*46
        self.cache[0] = 0
        self.cache[1] = 1
        self.cache[2] = 2
        self.cache[3] = 3

    def climbStairs(self, n: int) -> int:
        if self.cache[n] is None:
            self.cache[n] = self.climbStairs(n-1) + self.climbStairs(n-2)

        return self.cache[n]
