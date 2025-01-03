# 2025-01-01: following dynamic programming explore card

class Solution:
    def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
        n = len(jobDifficulty)

        if n < d:
            return -1

        dp = [[float("inf")] * (d + 1) for _ in range(n)]

        dp[-1][d] = jobDifficulty[-1]

        for i in range(n - 2, -1, -1):
            dp[i][d] = max(dp[i + 1][d], jobDifficulty[i])

        for day in range(d - 1, 0, -1):
            for i in range(day - 1, n - (d - day)):
                hardest = 0
                for j in range(i, n - (d - day)):
                    hardest = max(hardest, jobDifficulty[j])
                    dp[i][day] = min(dp[i][day], hardest + dp[j + 1][day + 1])
        return dp[0][1]
    # top-down approach (from dynamic programming gcard)
    def minDifficulty_topdown(self, jobDifficulty: List[int], d: int) -> int:
        n = len(jobDifficulty)

        if n < d:
            return -1

        hardest_job_remaining = [0] * n
        hardest_job = 0
        for i in reversed(range(n)):
            hardest_job = max(hardest_job, jobDifficulty[i])
            hardest_job_remaining[i] = hardest_job

        @lru_cache(None)
        def dp(i, day):
            if day == d:
                return hardest_job_remaining[i]
            best = float('inf')
            hardest = 0
            for j in range(i, n - (d - day)):
                hardest = max(hardest, jobDifficulty[j])
                best = min(best, hardest + dp(j + 1, day + 1))
            return best
        return dp(0, 1)
