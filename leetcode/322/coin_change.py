# 2024-11-21 Identified quickly that it was dynamic
# programming, but I didn't really grok it enough to get
# it correctly on my own.

from functools import lru_cache

class Solution:
    # bottom-up dynamic programming
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

    # dynamic programming: top-down
    def coinChange_dp_topdown(self, coins: List[int], amount: int) -> int:
        @lru_cache(None)
        def dfs(rem):
            if rem < 0:
                return -1

            if rem == 0:
                return 0

            min_cost = float('inf')

            for coin in coins:
                res = dfs(rem - coin)
                if res != -1:
                    min_cost = min(min_cost, res + 1)

            return min_cost if min_cost != float('inf') else -1
        return dfs(amount)
    # brute force
    def coinChange_brute_force(self, coins: List[int], amount: int) -> int:
        n = len(coins)

        def dfs(idx, amount):
            if amount == 0:
                return 0
            if idx < n and amount > 0:
                min_cost = float('inf')
                for x in range(amount // coins[idx] + 1):
                    res = dfs(idx + 1, amount-x * coins[idx])
                    if res != -1:
                        min_cost = min(min_cost, res + x)
                return -1 if min_cost == float('inf') else min_cost
            return -1

        return dfs(0, amount)
