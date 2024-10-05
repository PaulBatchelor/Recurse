from typing import List
from copy import deepcopy
from pprint import pprint

class Solution:
    def backtrack(self, prefix, remain, out):
        if len(remain) == 0:
            out.append(deepcopy(prefix))
        for r in remain:
            new_prefix = prefix + [r]
            new_remain = deepcopy(remain)
            new_remain.remove(r)
            self.backtrack(new_prefix, new_remain, out)

    # note: I do not love this version, as it involves
    # a lot of copying
    def permute(self, nums: List[int]) -> List[List[int]]:
        out = []
        self.backtrack([], set(nums), out)
        return out

def test(s):
    o = s()
    res = o.permute([1, 2, 3])
    expected = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    assert(res == expected)

    res = o.permute([0, 1])
    expected = [[0, 1], [1, 0]]
    assert(res == expected)

test(Solution)
