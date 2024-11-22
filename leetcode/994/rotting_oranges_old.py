from collections import deque
class Solution(object):
    def orangesRotting(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        m = len(grid)
        n = len(grid[0])
        minutes = 0
        q = deque()
        nfresh = 0
        visited = set()

        # get the total number of fresh oranges. If they are
        # adjacent to rotting oranges, push onto queue: x, y, minute
        # TL -> BR traversal. only the previous top and left neighbors
        # should be checked

        for row in range(0, m):
            for col in range(0, n):
                if grid[row][col] == 1:
                    nfresh += 1

                    rotten_left = col > 0 and grid[row][col - 1] == 2
                    rotten_up = row > 0 and grid[row - 1][col] == 2

                    if rotten_left or rotten_up:
                        q.append((row, col, 1))

        # pop items off queue while non-empty
        # make sure it hasn't been already visited
        # subtract from total number of oranges. if zero,
        # break.
        # update minutes, if needed
        # check and see if right and bottom neighbors are fresh.
        # push onto queue

        while len(q) > 0:
            o = q.popleft()
            (row, col, curtime) = o
            coord = row * n + col
            if coord in visited:
                continue
            visited.add(coord)
            nfresh -= 1
            minutes = max(curtime, minutes)
            if nfresh == 0:
                break

            fresh_down = row < (m - 1) and grid[row + 1][col] == 1
            fresh_right = col < (n - 1) and grid[row][col + 1] == 1

            if fresh_down:
                q.append((row + 1, col, curtime + 1))
            if fresh_right:
                q.append((row, col + 1, curtime + 1))

        # if there are still oranges left, return -1, otherwise
        # mintues

        if nfresh > 0:
            return -1
        return minutes
