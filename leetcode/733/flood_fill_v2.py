# Version 2, utilizing BFS instead of recursion

from collections import deque
from pprint import pprint

class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        q = deque()
        visited = set()
        q.append((sr, sc))
        m = len(image)
        n = len(image[0])
        target = image[sr][sc]
        image[sr][sc] = color
        
        while len(q) > 0:
            curnode = q.popleft()
            addr = curnode[0]*n + curnode[1]
            pprint(curnode)
            if addr in visited:
                continue
            visited.add(addr)
            offsets = [[1,0], [-1,0], [0, 1], [0, -1]]
            for (ro, co) in offsets:
                rpos = curnode[0] + ro
                cpos = curnode[1] + co
                if (rpos >= 0 and rpos < m) and (cpos >= 0 and cpos < n):
                    node = image[rpos][cpos]
                    if node == target:
                        image[rpos][cpos] = color
                        q.append((rpos, cpos))
        return image
