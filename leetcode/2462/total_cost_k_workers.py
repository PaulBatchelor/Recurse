# My solution feels inefficient, but correct. Going to
# implement this to see if I'm missing anything, then
# I'll check the answer. This is supposed to be a heap
# problem, so I get the feeling that I'm missing something
# in my approach because mine is essentially brute force

# note: candidates/k have been swapped
def brute_force(costs, candidates, k):
    k = min(k, len(costs))
    sum = 0
    N = len(costs)

    for c in range(0, candidates):
        min_left = costs[0]
        min_left_idx = 0

        min_right = costs[len(costs) - 1]
        min_right_idx = len(costs) - 1
        for i in range(0, k):
            lpos = i
            rpos = N - 1 - i

            lval = costs[lpos]
            rval = costs[rpos]

            if lval < min_left:
                min_left = lval
                min_left_idx = lpos

            if rval < min_right:
                min_right = rval
                min_right_idx = rpos

   
        selidx = min_left_idx
        if min_right == min_left:
            selidx = min_left_idx
        if min_right < min_left:
            selidx = min_right_idx
       
        val = costs.pop(selidx)
        sum += val
        N = len(costs)
        k = min(k, N)

    return sum


# 2 priority solution, adapted from the editorial

import heapq

def pq2(costs, k, candidates):
    m = candidates
    head_workers = []
    tail_workers = []

    next_head = m
    next_tail = len(costs) - m - 1
    sum = 0
    heapq.heapify(head_workers)
    heapq.heapify(tail_workers)

    for i in range(0, m):
        heapq.heappush(head_workers, costs[i])
        heapq.heappush(tail_workers, costs[len(costs) - 1 - i])

    for _ in range(0, k):
        # is there a way to peek?
        head = heapq.heappop(head_workers)
        tail = heapq.heappop(tail_workers)

        if head == tail:
            # put tail back
            heapq.heappush(tail_workers, tail)
            heapq.heappush(head_workers, costs[next_head])
            next_head += 1
            sum += head
        elif head < tail:
            heapq.heappush(tail_workers, tail)
            heapq.heappush(head_workers, costs[next_head])
            next_head += 1
            sum += head
        else:
            heapq.heappush(head_workers, head)
            heapq.heappush(tail_workers, costs[next_tail])
            next_tail -= 1
            sum += tail

    return sum



out = brute_force([17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4)
assert(out == 11)

out = pq2([17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4)
assert(out == 11)

out = brute_force([1, 2, 4, 1], 3, 3)
assert(out == 4)
