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

# This is adapted from the editorial. A little bit
# cleaner than the guess I made

def kmax2(nums, k):
    h = []
    heapq.heapify(h)

    for n in nums:
        heapq.heappush(h, n)
        if len(h) == k:
            heapq.heappop(h)

    return heapq.heappop(h)

out = kmax([3, 2, 1, 5, 6, 4], 2)
assert(out == 5)

out = kmax2([3, 2, 1, 5, 6, 4], 2)
assert(out == 5)
