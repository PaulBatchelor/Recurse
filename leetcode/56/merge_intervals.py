# I get the feeling I'm missing the point of this one.
def merge(self, intervals: List[List[int]]) -> List[List[int]]:
    out = []
    intervals = sorted(intervals)
    last = intervals[0]
    for ivl in intervals[1:]:
        if ivl[0] <= last[1]:
            last[1] = max(ivl[1], last[1])
        else:
            out.append(last)
            last = ivl
    out.append(last)
    return out
