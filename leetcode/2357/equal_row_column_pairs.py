# 2024-12-06 Brute forced it, couldn't see the hashmap
# problem, but was able to code it after reading the
# algorithm

class Solution:
    # based on editorial
    def equalPairs(self, grid: List[List[int]]) -> int:
        grid = [tuple(row) for row in grid]
        counts = Counter(grid, default=0)

        nequal = 0
        for c in range(len(grid)):
            col = []
            for r in range(len(grid)):
                col.append(grid[r][c])
            col = tuple(col)
            nequal += counts[col]
        return nequal

    # okay, this was just brute force
    def equalPairsV1(self, grid: List[List[int]]) -> int:
        cols = []

        for c in range(len(grid)):
            col = []
            for r in range(len(grid)):
                col.append(grid[r][c])
            cols.append(col)
        nequal = 0

        for row in grid:
            for col in cols:
                nequal += int(row == col)

        return nequal
