# 2024-12-06: this was more of a "do you know python" problem
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        cnt = Counter(arr)
        occ = set([x for _,x in cnt.items()])
        return len(occ) == len(cnt)
