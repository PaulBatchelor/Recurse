# 2024-11-16: Attempted solving with dynamic programming
# this works with the initial test cases, but fails with
# others
from pprint import pprint
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        out = []
        # boolean tables
        m = len(heights)
        n = len(heights[0])
        pacific = [[False]*n for _ in range(m)]
        atlantic = [[False]*n for _ in range(m)]

        # set up pacific table
        for c in range(n):
            pacific[0][c] = True

        for r in range(m):
            pacific[r][0] = True

        for r in range(1, m):
            for c in range(1, n):
                h = heights[r][c]
                # north
                if h >= heights[r - 1][c] and pacific[r-1][c]:
                    pacific[r][c] = True
                # west
                elif h >= heights[r][c-1] and pacific[r][c-1]:
                    pacific[r][c] = True
                # TODO: look east
                elif c < (n - 1) and h >= heights[r][c + 1] and pacific[r - 1][c + 1]:
                    pacific[r][c] = True

                # TODO: maybe not south?
                else:
                    pacific[r][c] = False

        # set up atlantic table

        for r in range(m):
            atlantic[r][n - 1] = True

        for c in range(n):
            atlantic[m-1][c] = True

        for r in range(1, m):
            r = m - r - 1
            for c in range(1, n):
                c = n - c - 1
                h = heights[r][c]
                if h >= heights[r + 1][c] and atlantic[r + 1][c]:
                    atlantic[r][c] = True
                elif h >= heights[r][c + 1] and atlantic[r][c + 1]:
                    atlantic[r][c] = True
                elif c > 0 and h >= heights[r][c-1] and atlantic[r + 1][c -1]:
                    atlantic[r][c] = True
                # TODO one other directional check
                else:
                    atlantic[r][c] = False

        # Pacific AND Atlantic
        for r in range(m):
            for c in range(n):
                if pacific[r][c] and atlantic[r][c]:
                    out.append([r, c])

        pprint(pacific)
        pprint(atlantic)
        return out

# Dynamic programming problem?
# Figure out which ones flow into pacific
# Figure out which ones flow into atlantic
# Find intersection between the two

# 1 2 2 3 5
# 3 2 3 4 4
# 2 4 5 3 1
# 6 7 1 4 5
# 5 1 1 2 4

# Pacific
# T T T T T
# T T T T T
# T T T F F
# T T F F F
# T F F F F

# Atlantic
# F F F F T
# F F F T T
# F F T T T
# T T T T T
# T T T T T

# Atlantic AND Pacific
# F F F F T
# F F F T T
# F F T F F
# T T F F F
# T F F F F

# 1 2 3
# 8 9 4
# 7 6 5
