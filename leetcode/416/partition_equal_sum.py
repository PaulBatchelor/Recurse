from pprint import pprint
from typing import List

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        n = len(nums)
        K = sum(nums)
        P = []

        if (K % 2 == 1):
            return False

        for _ in range((K//2)+1):
            P.append([None]*(n + 1))

        for x in range(0, n + 1):
            P[0][x] = True

        for x in range(0, (K//2) + 1):
            if x == 0:
                P[x][0] = True
            else:
                P[x][0] = False

        for i in range(1, (K//2) + 1):
            for j in range(1, n + 1):
                x = nums[j - 1]
                if (i - x) >= 0:
                    P[i][j] = P[i][j - 1] or P[i-x][j-1]
                else:
                    P[i][j] = P[i][j - 1]

        pprint(P)
        return P[K//2][n]

s = Solution()

rc = s.canPartition([1, 2, 3, 5])
pprint(rc)
# rc = s.canPartition([3, 1, 1, 2, 2, 1])
# pprint(rc)
