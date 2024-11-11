# 2024-11-11 I came up with 1.5 valid solutions that
# were too slow. Hours into it, I remembered that this
# may have shown up on a LC75 problem I didn't know.
# sure enough, I had to learn about a monotonically
# increasing stack. 20 minutes later I had the solution.
# good grief.

import heapq
class Solution:
    # monotonically increasing stack problem according to LC75, so I looked
    # up what those were all about. I didn't know about this data structure
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        s = []
        s.append(0)
        N = len(temperatures)
        out = [0]*N
        for i in range(len(temperatures)):
            while len(s) > 0 and temperatures[s[-1]] < temperatures[i]:
                j = s.pop()
                out[j] = i - j
            s.append(i)
        return out

    # possible efficiency gains using a priority queue
    def dailyTemperatures3(self, temperatures: List[int]) -> List[int]:
        pq = []
        for i, t in enumerate(temperatures):
            heapq.heappush(pq, (-t, i))

        N = len(temperatures)        
        out = [0]*len(temperatures)
        processed = []

        while len(pq) > 0:
            elem = heapq.heappop(pq)
            #print(elem[0], elem[1])
            next_pos = N + 1
            for p in processed:
                if -p[0] > -elem[0] and p[1] >= elem[1]:
                    next_pos = min(next_pos, p[1])
            processed.append(elem)
            if next_pos < N:
                out[elem[1]] = next_pos - elem[1]
        return out
    # might as well implement brute force
    def dailyTemperatures2(self, temperatures: List[int]) -> List[int]:
        N = len(temperatures)
        out = [0]*N
        for i in range(N):
            for j in range(i + 1, N):
                if temperatures[j] > temperatures[i]:
                    out[i] = j - i
                    break
        return out


# naive way: brute force. for each temperature at position i, iterate
# through i + 1 .. N - 1 temperatures until greater value found
# N + N - 1 + N - 2 .. 1

# maybe there's something to be said about working backwards or two-pointer
