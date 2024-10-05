# this took way too long to figure out

from collections import deque
from copy import deepcopy

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        out = []
        q = deque()
        curidx = 0
        candidates = sorted(candidates)
        q.append(candidates[curidx])
        while len(q) > 0 and curidx < len(candidates):
            total = sum(q)
            if total > target:
                val = q.popleft()
                if len(q) > 0 and val == q[-1]:
                    curidx += 1
                    #out.append(candidates[curidx])
            elif total == target:
                out.append(deepcopy(q))
                val = q.popleft()
                if len(q) > 0 and val == q[-1]:
                    curidx += 1
                    #out.append(candidates[curidx])
            else:
                q.append(candidates[curidx])
        return out
