# 2024-12-19: concept was right, but I had to tweak the
# details. My intuition on boundaries was wrong, and I
# forgot about copying over the array.
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        out = []
        def backtrack(combo, start):
            if len(combo) == k:
                total = sum(combo)
                if total == n:
                    out.append(combo.copy())
                return
            for i in range(start, 10):
                combo.append(i)
                backtrack(combo, i + 1)
                combo.pop()
        backtrack([], 1)
        return out
