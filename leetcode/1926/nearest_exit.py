# 2024-12-13: in my mind, there's really one way to do this
# one. LC says it wasn't that fast, but oh well it works

from collections import deque
class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        nrows, ncols = len(maze), len(maze[0])
        q = deque()
        visited = set()

        q.append((entrance, 0))

        min_steps = -1
        visited.add(tuple(entrance))
        while q:
            position, nsteps = q.popleft()
            row, col = position
            for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                rpos = row + d[0]
                cpos = col + d[1]

                if rpos < 0 or rpos >= nrows or cpos < 0 or cpos >= ncols:
                    continue
                pos = (rpos, cpos)
                # walkable?
                if maze[rpos][cpos] == '+':
                    continue
                if pos in visited:
                    continue

                # found edge?
                if rpos == 0 or rpos == nrows - 1 or cpos == 0 or cpos == ncols - 1:
                    if min_steps < 0:
                        min_steps = nsteps + 1
                    else:
                        min_steps = min(min_steps, nsteps + 1)

                visited.add(pos)
                q.append((pos, nsteps + 1))

        return min_steps
