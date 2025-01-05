
# 2025-01-05: read skiena and adapted it
# to a top-down DP solution. bottoms-up solution is WIP
class Solution:
    # bottoms-up solution (WIP)
    def minDistance_bottomsup(self, word1: str, word2: str) -> int:
        if len(word1) == 0 or len(word2) == 0:
            return max(len(word1), len(word2))

        dp = [[0]*len(word2) for _ in range(len(word1))]

        dp[0][0] = int(word1[0] != word2[0])

        for i in range(len(word1)):
            for j in range(len(word2)):
                # TODO: I think we need to initialize with values?
                continue

        for i in range(1, len(word1)):
            for j in range(1, len(word2)):
                if word1[i] == word2[j]:
                    match = dp[i - 1][j - 1]
                else:
                    match = dp[i - 1][j - 1] + 1
            
                insertion = dp[i - 1][j] + 1
                deletion = dp[i][j - 1] + 1
                dp[i][j] = min(match, insertion, deletion)
                
        return dp[len(word1) - 1][len(word2) - 1]
    # top down solution
    def minDistance(self, word1: str, word2: str) -> int:
        if len(word1) == 0 or len(word2) == 0:
            return max(len(word1), len(word2))
        @lru_cache(None)
        def dp(i, j):
            if i < 0:
                return j + 1
            if j < 0:
                return i + 1
    
            match = None
            if word1[i] == word2[j]:
                match = dp(i - 1, j - 1)
            else:
                match = dp(i - 1, j - 1) + 1
            
            insertion = dp(i - 1, j) + 1
            deletion = dp(i, j - 1) + 1

            return min(match, insertion, deletion)
        return dp(len(word1) - 1, len(word2) - 1) 

