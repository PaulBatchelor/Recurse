# this is my first priority queue problem, and I've never
# really worked with these data structures before.
# I think I have most of a working solution that works
# in linear time, so I want to use this as an opportunity
# to explore the python standard libary priority queue

import heapq

def kmax(nums, k):
    h = []
    heapq.heapify(h)
    kmax = None

    for n in nums:
        if len(h) == 0:
            kmax = n
            heapq.heappush(h, n)
        elif len(h) == k:
            kmax = heapq.heappop(h)
        if len(h) < k and n > kmax:
            heapq.heappush(h, n)

    if len(h) == k:
        kmax == heapq.heappop(h)

    return kmax

out = kmax([3, 2, 1, 5, 6, 4], 2)
assert(out == 5)
