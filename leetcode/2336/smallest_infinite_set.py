# 2024-12-15: my answer. Did not try to optimize. Did
# not get it right on first submit.
# The thing to realize about this one: any time you
# subtract something, you set a monotonically increasing
# counter. Any time you add something, it goes into a
# heap.

class SmallestInfiniteSet:
    def __init__(self):
        self.h = []
        self.max_so_far = 0

    def popSmallest(self) -> int:
        val = self.max_so_far + 1
        if self.h and self.h[0] <= val:
            val = heapq.heappop(self.h)

        while self.h and val == self.h[0]:
            heapq.heappop(self.h)

        self.max_so_far = max(self.max_so_far, val)
        # heapq.heappush(self.h, val + 1)
        return val

    def addBack(self, num: int) -> None:
        heapq.heappush(self.h, num)
