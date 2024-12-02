# 2024-12-02: not the fastest solution according to LC, but it passes

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if len(s) == 0:
            return True
        pos = 0
        for i in range(len(t)):
            if t[i] == s[pos]:
                pos += 1
                if pos == len(s):
                    return True
        return False
