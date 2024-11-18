# 01 matrix
# I see a BFS graph solution for each node. I'd definitely
# be interested in seeing if there exists better solutions
# for the problem

from collections import deque
from pprint import pprint

def find_nearest_zero(mat, nrows, ncols, r, c, dist):
    q = deque()
    newq = deque()

    newq.append((r, c))

    while len(newq) > 0:
        q = newq.copy()
        newq.clear()
        while len(q) > 0:
            pos = q.popleft()
            if mat[pos[0]][pos[1]] == 0:
                return dist

            rp1 = pos[0] + 1
            rm1 = pos[0] - 1
            cp1 = pos[1] + 1
            cm1 = pos[1] - 1

            # north
            if cm1 >= 0:
                newq.append((pos[0], cm1))
            # south
            if cp1 < ncols:
                newq.append((pos[0], cp1))
            # east
            if rp1 < nrows:
                newq.append((rp1, pos[1]))
            # west
            if rm1 >= 0:
                newq.append((rm1, pos[1]))

        dist += 1

    return -1

def matrix01(mat):
    out = []
    nrows = len(mat)
    ncols = len(mat[0])

    for r in range(0, nrows):
        currow = []
        for c in range(0, ncols):
            dist = find_nearest_zero(mat, nrows, ncols, r, c, 0)
            currow.append(dist)
        out.append(currow)
            


    return out

out = matrix01([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
assert(out == [[0, 0, 0], [0, 1, 0], [0, 0, 0]])

out = matrix01([[0, 0, 0], [0, 1, 0], [1, 1, 1]])
assert(out == [[0, 0, 0], [0, 1, 0], [1, 2, 1]])
