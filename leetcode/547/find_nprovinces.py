# 2024-12-13: got it right on the first try.

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        stk = []
        visited = set()
        ncities = len(isConnected)

        stk.append(0)
        visited.add(0)
        nprovinces = 0

        while stk:
            city = stk.pop()
            for i in range(ncities):
                if i != city and isConnected[city][i] == 1 and i not in visited:
                    visited.add(i)
                    stk.append(i)

            # nothing more to traverse, find next available city
            if not stk:
                nprovinces += 1
                for i in range(ncities):
                    if i not in visited:
                        stk.append(i)
                        visited.add(i)
                        break

        return nprovinces
