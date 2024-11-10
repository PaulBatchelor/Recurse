# 2024-11-10: struggled a bit with a few approaches that
# didn't work with all the edge cases, used the priority
# queue hint to work through the answer. the keyword about
# "cycles" was helpful
from collections import Counter
import heapq
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        pq = []
        cycles = -1
        last_count = 0
        counts = Counter(tasks)
        # create initial priority queue. larger counts float
        # up top
        for task in counts:
            heapq.heappush(pq, -counts[task])
        while len(pq) > 0:
            cycles += 1
            # extract at most n + 1
            last_count = min(n + 1, len(pq))
            instr = []
            for _ in range(last_count):
                instr.append(heapq.heappop(pq))
            for i in instr:
                # negative number hack to make maxheap, so count up
                i += 1
                if i < 0:
                    heapq.heappush(pq, i)
        return cycles * (n + 1) + last_count
