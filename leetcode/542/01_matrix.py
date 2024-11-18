# 2024-11-18: BFS solution. Submitted to LC and confirmed
# to work.
from collections import deque
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        q = deque()
        nrows = len(mat)
        ncols = len(mat[0])
        distances = [[-1]*ncols for _ in range(nrows)]

        # place all 0s onto stack
        for r in range(nrows):
            for c in range(ncols):
                if mat[r][c] == 0:
                    distances[r][c] = 0
                    q.append((r, c))

        # BFS using queue
        while len(q) > 0:
            cell = q.popleft()
            cell_r, cell_c = cell
            dist = distances[cell_r][cell_c]

            for offr, offc in [[1,0], [0,1], [-1,0], [0,-1]]:
                new_r = cell_r + offr
                new_c = cell_c + offc

                if new_r < 0 or new_r >= nrows or new_c < 0 or new_c >= ncols:
                    continue

                # distance already found, ignore
                if distances[new_r][new_c] >= 0:
                    continue

                val = mat[new_r][new_c]
                if val == 1:
                    #print("found val")
                    distances[new_r][new_c] = dist + 1
                else:
                    distances[new_r][new_c] = 0

                q.append((new_r, new_c))

        return distances
