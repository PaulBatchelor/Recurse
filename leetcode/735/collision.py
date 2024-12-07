# 2024-12-07 I had what I thought was a really solid solution
# right up until the edge case where asteroids where going
# in opposite directions but not colliding. I was
# working under the assumption that ANY change in directoin
# would be a collision (which is wrong). Once again,
# my left/right dyslexia strikes again.

class Solution:
    # fed into claude, hand-transcribed
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stk = []
        for ast in asteroids:
            while stk and ast < 0 < stk[-1]:
                if stk[-1] < -ast:
                    stk.pop()
                    continue
                elif stk[-1] == -ast:
                    stk.pop()
                break
            else:
                stk.append(ast)

        return stk

    def asteroidCollisionV1(self, asteroids: List[int]) -> List[int]:
        stk = []
        left = True
        right = False
        for ast in asteroids:
            stk.append(ast)
            while len(stk) > 1:
                a1 = stk.pop()
                a2 = stk.pop()

                a1dir = a1 < 0
                a2dir = a2 < 0

                # same direction
                if a1dir == a2dir or (a2dir == left and a1dir == right):
                    stk.append(a2)
                    stk.append(a1)
                    break

                # collision: skip pushing to stack
                if abs(a1) == abs(a2):
                    continue

                # push greater size
                stk.append(a1 if abs(a1) > abs(a2) else a2)
        return stk

