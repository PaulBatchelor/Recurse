# 2024-12-07: The hardest part was understanding the problem.
# I'm still thinking that list(stk) will do what I want,
# even though it's "".join(stk).
class Solution:
    def removeStars(self, s: str) -> str:
        stk = []
        for ch in s:
            if ch == '*':
                stk.pop() if stk else None
                continue
            stk.append(ch)
        return "".join(stk)
