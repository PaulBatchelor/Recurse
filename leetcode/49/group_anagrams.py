# 2024-11-13 Pretty much got it on the first try. I started
# going into Counter() territory and doing comparisons,
# but sorting keys and using a hashmap made more sense for
# the grouping component

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}

        for i in range(len(strs)):
            key = str(sorted(strs[i]))
            if key in groups:
                groups[key].append(i)
            else:
                groups[key] = [i]
        out = []

        for k,v in groups.items():
            g = []
            for i in v:
                g.append(strs[i])
            out.append(g)

        return out


