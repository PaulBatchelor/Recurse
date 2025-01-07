# 2025-01-07: worked out DFS solution
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        nrows, ncols = len(board), len(board[0])
        def dfs(pos, i, visited=set()):
            row, col = pos

            if board[row][col] != word[i]:
                return False

            if i == len(word) - 1:
                return True

            visited.add(pos)
            for d in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nxtrow = row + d[0]
                nxtcol = col + d[1]

                if nxtrow < 0 or nxtrow >= nrows or nxtcol < 0 or nxtcol >= ncols:
                    continue
                
                nxtpos = (nxtrow, nxtcol)
                if nxtpos in visited:
                    continue
                if dfs(nxtpos, i + 1, visited):
                    return True

            visited.remove(pos)
            return False
        
        for row in range(nrows):
            for col in range(ncols):
                if board[row][col] == word[0]:
                    if dfs((row, col), 0):
                        return True
        
        return False

class Solution:
    def traverse(self, pos, board, word, visited):
        # if current word pos not equal to target, false
        target = word[pos[2]]
        if board[pos[0]][pos[1]] != target:
            return False

        # if current target is last, return true
        if pos[2] == len(word) - 1:
            return True

        # mark target as visited
        visited[pos[0]][pos[1]] = True

        # DFS 4 cardinal directions
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        m = len(board)
        n = len(board[0])

        for d in dirs:
            r = pos[0] + d[0]
            c = pos[1] + d[1]
            
            if r < 0 or r >= m:
                continue
            if c < 0 or c >= n:
                continue
            if visited[r][c]:
                continue

            ret = self.traverse((r, c, pos[2] + 1), board, word, visited)
            if ret:
                return True

        # unmark target as visited
        visited[pos[0]][pos[1]] = False

        return False

    def exist(self, board: List[List[str]], word: str) -> bool:
        candidates = []
        m = len(board)
        n = len(board[0])

        visited = [[False]*n for _ in range(m)]

        for r in range(m):
            for c in range(n):
                if board[r][c] == word[0]:
                    candidates.append((r, c, 0))
        for pos in candidates:
            if self.traverse(pos, board, word, visited):
                return True
        return False
