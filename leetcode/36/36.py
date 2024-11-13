# 2024-11-13: "sudoku" is a bit of a misnomer. In the hints,
# it said a board could be "valid" but "unsolveable",
# meaning it's really just a set problem. Also, note
# that it says "valid", not "solver".
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # check rows for distinct values
        for r in range(9):
            currow = set()
            for c in range(9):
                if board[r][c] == '.':
                    continue
                val = board[r][c]
                if val in currow:
                    return False
                currow.add(val)

        # check columns for distinct values
        for c in range(9):
            curcol = set()
            for r in range(9):
                val = board[r][c]
                if val == '.':
                    continue
                if val in curcol:
                    return False
                curcol.add(val)

        # check boxes for distinct values
        for box in range(9):
            curbox = set()
            brow = (box // 3) * 3
            bcol = (box % 3) * 3
            for i in range(9):
                r = brow + (i // 3)
                c = bcol + (i % 3)
                val = board[r][c]
                if val == '.':
                    continue
                if val in curbox:
                    return False
                curbox.add(val)

        return True
