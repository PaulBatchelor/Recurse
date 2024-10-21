# 2024-10-21: I came in with a tedious to code solution, but
# it seems to perform quite well. A graph traversal algo
# may have been easier?
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        # constrained traversal problem
        # movement goes left -> down -> right -> up -> left
        # move in a given direction until you hit a boundary (edge or previously visited),
        # then change direction

        # instead of keeping track of nodes, maybe realize the pattern?
        # m = nrows, n = ncols
        # m=3, n=4
        # move 3 left (n - 1)
        # move 2 down (m - 1)
        # move 3 right (n - 1)
        # move 1 up (m - 2)
        # move 2 left (n - 2)

        # m=3, n=3
        # move 2 right
        # move 2 down
        # move 2 left
        # move 1 up

        # m=4, n=4
        # right 3
        # down 3
        # left 3
        # up 2
        # right 2
        # down 1
        # left 1

        # # # #
        # # # #
        # # # #
        # # # #

        m = len(matrix)
        n = len(matrix[0])

        out = []
        dir = "right"
        pos = [0, 0]
        remaining = n * m
        movec = n - 1
        mover = m - 1
        counter = movec

        movement = {

            "right": [0, 1],
            "left": [0, -1],
            "up": [-1, 0],
            "down": [1, 0]
        }


        print(f"{dir} {counter}")
        while remaining > 0:
            #print(f"counter: {counter}")
            if counter == 0:
                if dir == "right":
                    dir = "down"
                    counter = mover
                    mover -= 1
                elif dir == "down":
                    dir = "left"
                    counter = movec
                    movec -= 1
                elif dir == "left":
                    dir = "up"
                    counter = mover
                    mover -= 1
                elif dir == "up":
                    dir = "right"
                    counter = movec
                    movec -= 1
                # hacky
                #if counter == 0:
                #    break
                print(f"{dir} {counter}")

            out.append(matrix[pos[0]][pos[1]])

            d = movement[dir]
            pos[0] += d[0]
            pos[1] += d[1]
            counter -= 1
            remaining -= 1

        return out
