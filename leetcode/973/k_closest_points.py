# 2024-11-18 My new solution for this, that actually was
# submitted to LC
import heapq
import math
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        if k == len(points):
            return points

        h = [(-math.sqrt(p[0]*p[0] + p[1]*p[1]), p) for p in points[:k]]
        heapq.heapify(h)

        for p in points[k:]:
            heapq.heappush(h,(-math.sqrt(p[0]*p[0] + p[1]*p[1]), p))
            heappop(h)

        return [x[1] for x in h]
