# 2024-11-16: I was expected to handle the obstacles
# more carefully, but it looks like this works just fine

from collections import deque
class Solution:
    def getFood(self, grid: List[List[str]]) -> int:
        nrows, ncols = len(grid), len(grid[0])
        q = deque()

        distances = [[-1]*ncols for _ in range(nrows)]

        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == '#':
                    q.append((r, c))
                    distances[r][c] = 0

        player = (-1, -1)

        while q:
            row, col = q.popleft()
            curdist = distances[row][col]

            #print(row, col)
            for (r, c) in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                new_row = row + r
                new_col = col + c

                if new_row < 0 or new_row >= nrows or new_col < 0 or new_col >= ncols:
                    continue

                # check for obstacles

                if grid[new_row][new_col] == 'X':
                    continue

                if grid[new_row][new_col] == '*':
                    player = (new_row, new_col)

                # already visited, pick the smallest
                if distances[new_row][new_col] >= 0:
                    distances[new_row][new_col] = min(curdist + 1, distances[new_row][new_col])
                    continue

                distances[new_row][new_col] = curdist + 1
                q.append((new_row, new_col))

        return distances[player[0]][player[1]]
