# 2025-01-01: Following dynamic programming explore card

class Solution:
    # bottoms up
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        t1len, t2len = len(text1), len(text2)

        dp = [[0] * (t2len + 1) for _ in range(t1len + 1)]

        for i in reversed(range(t1len)):
            for j in reversed(range(t2len)):
                if text1[i] == text2[j]:
                    dp[i][j] = max(1 + dp[i + 1][j + 1], dp[i][j + 1], dp[i + 1][j + 1])
                else:
                    dp[i][j] = max(dp[i][j + 1], dp[i + 1][j])

        return dp[0][0]

    def longestCommonSubsequenceV1(self, text1: str, text2: str) -> int:
        t1len, t2len = len(text1), len(text2)
        @cache
        def dp(i, j):
            if i == t1len:
                return 0
            if j == t2len:
                return 0

            if text1[i] == text2[j]:
                match_one = 1 + dp(i + 1, j + 1)
                match_two = dp(i, j + 1)
                match_three = dp(i + 1, j)
                return max(match_one, match_two, match_three)

            x = dp(i, j + 1)
            y = dp(i + 1, j)
            return max(x, y)

        return dp(0, 0)


# 2024-12-27 So close to getting it right

class Solution:
    # editorial
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        t = [[0] * (len(text2) + 1) for _ in range(len(text1) +1)]
        for col in reversed(range(len(text2))):
            for row in reversed(range(len(text1))):
                if text2[col] == text1[row]:
                    t[row][col] = 1 + t[row + 1][col + 1]
                else:
                    t[row][col] = max(t[row + 1][col], t[row])
        return t[0][0]

    # my initial approach. I was *so* close to getting it
    # right. The bad line of code was commented out
    def longestCommonSubsequenceV1(self, text1: str, text2: str) -> int:
        text1 = " " + text1
        text2 = " " + text2
        t = [[0]*(len(text1)) for _ in range(len(text2))]

        for i in range(1, len(text2)):
            for j in range(1, len(text1)):
                #t[i][j] = int(text1[j] == text2[i])
                if text1[j] == text2[i]:
                    # incorrect line
                    #t[i][j] = 1 + max(t[i - 1][j], t[i][j - 1])
                    t[i][j] = 1 + t[i - 1][j - 1]
                else:
                    t[i][j] = max(t[i - 1][j], t[i][j - 1])
        return t[len(text2) - 1][len(text1) - 1]1
