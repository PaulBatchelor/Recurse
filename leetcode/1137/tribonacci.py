# 2025-01-01: working through dynamic programming card

class Solution:
    # space optimized
    def tribonacci(self, n: int) -> int:
        t = [0] * 3
        
        t[0] = 0
        t[1] = 1
        t[2] = 1
        
        for i in range(3, n + 1):
            tmp = t[2] + t[1] + t[0]
            t[0] = t[1]
            t[1] = t[2]
            t[2] = tmp

        if n < 2:
            return t[n]
        return t[2]
    
    def tribonacci_bottomsup_1(self, n: int) -> int:
        t = [0] * max(3, (n + 1))
        
        t[0] = 0
        t[1] = 1
        t[2] = 1
        
        if n <= 2:
            return t[n]
        
        for i in range(2, n + 1):
            t[i] = t[i - 1] + t[i - 2] + t[i - 3]
        
        return t[n]
    def tribonacci_topdown(self, n: int) -> int:
        def dp(i):
            if i == 0:
                return 0
            if i == 1:
                return 1
            if i == 2:
                return 1
            
            if i not in memo:
                memo[i] = dp(i - 1) + dp(i - 2) + dp(i - 3)
            return memo[i]
        
        memo = {}
        
        return dp(n)
            
# 2024-12-21: this reminds me of an IIR filter structure.
class Solution:
    def tribonacci(self, n: int) -> int:
        t0 = 0
        t1 = 1
        t2 = 1

        if n == 0:
            return t0
        elif n == 1:
            return t1
        elif n == 2:
            return t2

        t3 = t0 + t1 + t2
        for _ in range(3, n + 1):
            t3 = t0 + t1 + t2
            t0 = t1
            t1 = t2
            t2 = t3

        return t3
