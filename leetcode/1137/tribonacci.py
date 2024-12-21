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
