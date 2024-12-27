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
