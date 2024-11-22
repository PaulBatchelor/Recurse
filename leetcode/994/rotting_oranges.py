# 2024-11-22: my initial attempt was based off of the bFS
# solution in number of islands, but I got an error in
# the edge cases because I forgot to consider multiple
# oranges, so I pivoted to using a single BFS

from collections import deque
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        nrows = len(grid)
        ncols = len(grid[0])

        nfresh = 0
        nminutes = 0

        q = deque()

        # first get number of fresh oranges
        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == 1:
                    nfresh += 1
                if grid[r][c] == 2:
                    q.append((r, c, 0))

        while q:
            currow, curcol, curtime = q.popleft()

            nminutes = max(curtime, nminutes)
            for ro, co in ([1, 0], [-1, 0], [0, 1], [0, -1]):
                nxtrow = currow + ro
                nxtcol = curcol + co

                if nxtrow < 0 or nxtrow >= nrows or nxtcol < 0 or nxtcol >= ncols:
                    continue

                if grid[nxtrow][nxtcol] == 1:
                    grid[nxtrow][nxtcol] = 0
                    q.append((nxtrow, nxtcol, curtime + 1))
                    nfresh -= 1

        if nfresh > 0:
            return -1

        return nminutes

    def orangesRotting1(self, grid: List[List[int]]) -> int:
        nrows = len(grid)
        ncols = len(grid[0])

        nfresh = 0
        nminutes = 0

        # first get number of fresh oranges
        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == 1:
                    nfresh += 1

        # iterate again. If a rotten orange is found, perform BFS

        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == 2:
                    grid[r][c] = 0
                    q = deque()
                    q.append((r, c, 0))
                    while q:
                        row, col, mins = q.popleft()
                        nminutes = max(mins, nminutes)
                        for ro, co in ([1, 0], [0, 1], [-1, 0], [0, -1]):
                            nxtrow = row + ro
                            nxtcol = col + co

                            if nxtrow < 0 or nxtrow >= nrows or nxtcol < 0 or nxtcol >= ncols:
                                continue

                            if grid[nxtrow][nxtcol] == 1:
                                grid[nxtrow][nxtcol] = 0
                                q.append((nxtrow, nxtcol, mins + 1))
                                nfresh -= 1

        if nfresh > 0:
            return -1

        return nminutes

# 2 1 1
# 1 1 1
# 0 1 2
