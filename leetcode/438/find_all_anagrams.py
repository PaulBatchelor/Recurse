# 2024-11-03 sliding window using Counter
# apparently kind of slow on LC, probably
# the comparison could be improved, but it works
from collections import Counter
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # sliding window
        # create counter hashmap of p
        pcount = Counter(p)
        # create window, counter of first len(p) items of s
        scount = Counter(s[0:len(p)])
        out = []
        s_len = len(s)
        p_len = len(p)
        # iterate through s: 0-len(s)-len(p)
        print(s_len, p_len)
        for i in range(s_len - p_len + 1):
            #print(i)
            #pprint(scount)
            # if current window matches p counter, append indice to output
            if pcount == scount:
                out.append(i)
            # slide, remove element i, add i + len(p)
            scount.subtract(s[i])
            if (i + p_len) < s_len:
                scount.update(s[i + p_len])
        return out
