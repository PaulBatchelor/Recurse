# 2024-10-03: Is there a way to do traverse a grid like
# this without keeping track of visited nodes?
from collections import deque
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # this is a breadth-first traversal problem, ideally one
        # where each node is visited exactly once 

        # use a queue for BFS
        q = deque()
        m = len(grid)
        n = len(grid[0])

        # traversal goes top to down, left to right

        q.append((0, 0))

        nislands = 0

        # keep track of visited islands in a set.
        # I do not love this. It would be nice to be able to come up with a traverse
        # pattern that goes top-left to bottom-right reaching in the grid, reaching
        # every node exactly once
        visited = set()

        while len(q) > 0:
            pos = q.popleft()

            # TODO: use row/col instead of x/y
            x = pos[0]
            y = pos[1]
            next_x = x + 1
            next_y = y + 1
            prev_x = x - 1
            prev_y = y - 1
            val = grid[y][x]

            # islands are discovered in the top-left corner. so check and see if
            # there is one at (0, 0)

            coord = x * n + y * m
            if coord in visited:
                continue
            visited.add(coord)

            if x == 0 and y == 0 and val == "1":
                nislands += 1
            # the top-left corner of a new island is found if the upper and left neighbors are zero, and the current value is 1
            elif val == "1":
                upper_zero = prev_y < 0 or grid[prev_y][x] == "0"
                left_zero = prev_x < 0 or grid[y][prev_x] == "0"

                if upper_zero and left_zero:
                    nislands += 1

            if next_x < n:
                q.append((next_x, y))

            if next_y < m:
                q.append((x, next_y))

        return nislands
