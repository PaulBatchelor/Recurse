# 2025-01-01: looking at editorial
class Solution:
    # "better" solution
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        dp = [0] * (cols + 1)

        maxsqlen = 0
        prev = 0
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                temp = dp[j]
                if matrix[i - 1][j - 1] == '1':
                    dp[j] = min(min(dp[j - 1], prev), dp[j]) + 1
                    maxsqlen = max(maxsqlen, dp[j])
                else:
                    dp[j] = 0
                prev = temp
        return maxsqlen * maxsqlen

    # derived top-down approach from editorial
    def maximalSquare_topdown(self, matrix: List[List[str]]) -> int:
        @cache
        def dp(r, c):
            nonlocal maxsqlen
            if r < 0:
                return 0
            if c < 0:
                return 0

            if matrix[r][c] == '1':
                tmp = min(dp(r, c - 1), dp(r - 1, c))
                tmp = min(tmp, dp(r - 1, c - 1))
                tmp += 1
                maxsqlen = max(maxsqlen, tmp)
                return tmp
            # call recursively to traverse, but since it is zero
            # the size will always be 0
            dp(r, c - 1)
            dp(r - 1, c)
            return 0

        maxsqlen = 0
        nrows = len(matrix)
        ncols = len(matrix[0]) if nrows else 0

        dp(nrows - 1, ncols - 1)

        return maxsqlen * maxsqlen
    # bottoms-up DP solution
    def maximalSquareV1(self, matrix: List[List[str]]) -> int:
        nrows = len(matrix)
        ncols = len(matrix[0]) if nrows else 0

        dp = [[0] * (ncols + 1) for _ in range(nrows + 1)]
        maxsqlen = 0
        for r in range(1, nrows + 1):
            for c in range(1, ncols + 1):
                if matrix[r - 1][c - 1] == '1':
                    dp[r][c] = min(
                        min(dp[r][c - 1], dp[r - 1][c]),
                        dp[r - 1][c - 1]
                    ) + 1
                    maxsqlen = max(maxsqlen, dp[r][c])


        return maxsqlen * maxsqlen
