# 2024-12-21: My initial intuition was close, but ultimately
# missed the details. Below are the editorial for both top
# down and bottoms up. The '@cache' decorator seems to be
# built in the LC python instance.

class Solution:
    def numTilings(self, n: int) -> int:
        if n == 1:
            return 1
        elif n == 2:
            return 2

        f = [0] * (n + 1)
        p = [0] * (n + 1)

        f[1] = 1
        f[2] = 2
        p[2] = 1

        for k in range(3, n + 1):
            f[k] = (f[k - 1] + f[k - 2] + 2*p[k - 1]) % 1_000_000_007
            p[k] = (p[k - 1] + f[k - 2]) % 1_000_000_007

        return f[n]
    def numTilings_top_down(self, n: int) -> int:
        MOD = 1_000_000_007

        @cache
        def p(n):
            if n == 2:
                return 1
            return (p(n - 1) + f(n - 2)) % MOD

        @cache
        def f(n):
            if n <= 2:
                return n
            return (f(n - 1) + f(n - 2) + 2 * p(n - 1)) % MOD

        return f(n)


