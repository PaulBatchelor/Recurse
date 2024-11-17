# 2024-11-17: two solutions from the editorial.
# The brute force one was pretty intuitive conceptually, but I
# didn't know the python syntax. A heap did come to mind,
# but I didn't know how to maintian lexicographical order.
# turns out, it seems to do it for you already, and
# you don't have to worry about that?
from pprint import pprint
from collections import Counter
from heapq import heapify, heappop

class Solution:
    # max heap
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        # counter seems to be in lexicographical order
        heap = [(-freq, word) for word, freq in cnt.items()]


        # heapify must maintain lexicographical order somehow?
        heapify(heap)

        return [heappop(heap)[1] for _ in range(k)]
    # brute force
    def topKFrequent_bruteforce(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        # lambda syntax is confusing me:
        # 1. I'm assuming this implicitely returns the tuple (no return statement)
        # 2. how do tuples work in sort functions?
        out = sorted(list(cnt.keys()), key=lambda x: (-cnt[x], x))[:k]
        # pprint(out)
        return out
