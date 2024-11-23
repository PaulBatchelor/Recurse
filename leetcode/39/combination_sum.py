# 2024-11-23: Reminded me of a variant knapsack problem,
# which can typically be solved with dynamic programming.
# However, the problem isn't fine one optimal solution,
# but returning the results of many optimal solutions. So,
# it becomes a combinatorial problem solved with backtracking
class Solution:
    # studying the editorial solution, which seems slightly more optimized
    # attempting to use my existing variable names and patterns instead of theirs
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        out = []

        def backtrack(remain, combo, start):
            if remain == 0:
                out.append(combo.copy())
                return
            elif remain < 0:
                return

            for i in range(start, len(candidates)):
                combo.append(candidates[i])
                backtrack(remain - candidates[i], combo, i)
                combo.pop()
        backtrack(target, [], 0)
        return out
    def combinationSumV1(self, candidates: List[int], target: int) -> List[List[int]]:
        # backtracking combinatorial problem, knapsack problem
        out = []
        def backtrack(combo, start):
            total = sum(combo)
            if total > target:
                return
            if total == target:
                out.append(combo.copy())
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                combo.append(c)
                backtrack(combo, i)
                combo.pop()

        backtrack([], 0)
        return out
