# 2024-11-22 I knew pretty well you could use BFS to solve
# this, but I couldn't get the code together for it.
# I've included the very weird disjoint set solution here.
# I do not understand it.

from collections import deque

class UnionFind:
    def __init__(self, grid):
        self.count = 0
        m, n = len(grid), len(grid[0])
        self.parent = []
        self.rank = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    self.parent.append(i * n + j)
                    self.count += 1
                else:
                    self.parent.append(-1)
                self.rank.append(0)

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        rootx = self.find(x)
        rooty = self.find(y)

        if rootx != rooty:
            if self.rank[rootx] > self.rank[rooty]:
                self.parent[rooty] = rootx
            elif self.rank[rootx] < self.rank[rooty]:
                self.parent[rootx] = rooty
            else:
                self.parent[rooty] = rootx
                self.rank[rootx] += 1
            self.count -= 1

    def getCount(self):
        return self.count

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        nrows = len(grid)
        ncols = len(grid[0])

        uf = UnionFind(grid)

        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == "1":
                    grid[r][c] = "0"
                    for ro, co in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nxtrow = ro + r
                        nxtcol = co + c

                        if nxtrow < 0 or nxtrow >= nrows or nxtcol < 0 or nxtcol >= ncols:
                            continue

                        if grid[nxtrow][nxtcol] == "1":
                            uf.union(r * ncols + c, nxtrow * ncols + nxtcol)

        return uf.getCount()
    def numIslands_bfs(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        num_islands = 0

        nrows = len(grid)
        ncols = len(grid[0])

        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == "1":
                    num_islands += 1
                    q = deque()
                    q.append((r, c))
                    while q:
                        currow, curcol = q.popleft()
                        grid[currow][curcol] = "0"
                        for ro, co in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nxtrow = ro + currow
                            nxtcol = co + curcol
                            if nxtrow < 0 or nxtrow >= nrows or nxtcol < 0 or nxtcol >= ncols:
                                continue
                            if grid[nxtrow][nxtcol] == "1":
                                grid[nxtrow][nxtcol] = "0"
                                q.append((nxtrow, nxtcol))
        return num_islands
    def numIslands_dfs(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        num_islands = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "1":
                    self.dfs(grid, i, j)
                    num_islands += 1

        return num_islands
    def dfs(self, grid, r, c):
        if (
            r < 0
            or c < 0
            or r >= len(grid)
            or c >= len(grid[0])
            or grid[r][c] != "1"
        ):
            return
        grid[r][c] = "0"

        self.dfs(grid, r - 1, c)
        self.dfs(grid, r + 1, c)
        self.dfs(grid, r, c - 1)
        self.dfs(grid, r, c + 1)
