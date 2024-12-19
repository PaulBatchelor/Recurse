# 2024-12-19: Had a hard time getting all the pieces
# connected together properly. Had difficulty grokking
# the logic put in place to prevent overlap.

from pprint import pprint
class Solution:
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:
        head_workers = []
        tail_workers = []
        ncosts = len(costs)
        total = 0

        for i in range(candidates):
            heapq.heappush(head_workers, costs[i])

        start = max(candidates, ncosts - candidates)
        for i in range(start, ncosts):
            heapq.heappush(tail_workers, costs[i])

        # TODO: understand this
        # head_workers = costs[:candidates]
        # tail_workers = costs[max(candidates, len(costs) - candidates):]
        # heapq.heapify(head_workers)
        # heapq.heapify(tail_workers)

        pprint(len(head_workers))
        pprint(len(tail_workers))

        next_head = candidates
        next_tail = ncosts - candidates - 1

        for _ in range(k):
            if not tail_workers or head_workers and head_workers[0] <= tail_workers[0]:
                total += head_workers[0]
                heapq.heappop(head_workers)
                if next_head <= next_tail:
                    heapq.heappush(head_workers, costs[next_head])
                    next_head += 1
            else:
                total += tail_workers[0]
                heapq.heappop(tail_workers)
                if next_head <= next_tail:
                    heapq.heappush(tail_workers, costs[next_tail])
                    next_tail -= 1
        return total

    def totalCostV1(self, costs: List[int], k: int, candidates: int) -> int:
        left = []
        right = []
        nworkers = len(costs)
        total = 0
        visited = set()

        for _ in range(k):
            h = []
            for i in range(nworkers):
                if len(h) == candidates:
                    break
                if i not in visited:
                    heapq.heappush(h, (costs[i], i))
            for i in reversed(range(nworkers)):
                if len(h) == 2*candidates:
                    break
                if i not in visited:
                    heapq.heappush(h, (costs[i], i))
            mincost, worker = heapq.heappop(h)
            visited.add(worker)
            total += mincost

        return total
