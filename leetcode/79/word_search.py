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
