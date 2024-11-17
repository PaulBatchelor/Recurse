# 2024-11-17 Solved it pretty quickly because I had just
# done 692, so I worked through the other slicer options
# from the editorial

from collections import Counter
from heapq import heapify, heappop, heappush, nlargest

class Solution:
    # use python3 built-in nlargest function
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = Counter(nums)
        return nlargest(k, cnt.keys(), key=cnt.get)

    # use a heap of size K
    def topKFrequent_v2(self, nums: List[int], k: int) -> List[int]:    
        cnt = Counter(nums)
        h = []
        for num, c in cnt.items():
            heappush(h, (c, num))
            if len(h) > k:
                heappop(h)
        return [heappop(h)[1] for _ in range(k)]


    # pattern applied from 692
    def topKFrequent_v1(self, nums: List[int], k: int) -> List[int]:
        cnt = Counter(nums)
        heap = [(-amt, num) for num, amt in cnt.items()]
        heapify(heap)
        return [heappop(heap)[1] for _ in range(k)]
