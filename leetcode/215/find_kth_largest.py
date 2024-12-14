# 2024-12-13: been a minute since I did a heap problem,
# forgot how to use heapq.
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = []
        for i in range(len(nums)):
            heapq.heappush(h, nums[i])
            if i >= k:
                heapq.heappop(h)

        return heapq.heappop(h)
