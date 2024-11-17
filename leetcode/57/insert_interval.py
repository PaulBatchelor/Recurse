# 2024-11-17: stumbled into this solution, will want
# to look at the editorial for something more elegant
from pprint import pprint
class Solution:
    def overlap(self, a, b):
        # make sure a starts before b
        if a[0] > b[0]:
            tmp = a
            a = b
            b = tmp

        return (b[0] >= a[0] and b[0] <= a[1])

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        out = []
        for ivl in intervals:
            # check for overlap between lastInterval and newInterval
            # merge if there is overlap, and continue without appending

            #print(f"new interval: {newInterval[0], newInterval[1]}, ivl: {ivl[0], ivl[1]}")
            # look for overlap in start times

            if (newInterval is not None and self.overlap(newInterval, ivl)):
                # merge intervals
                newInterval[0] = min(ivl[0], newInterval[0])
                newInterval[1] = max(ivl[1], newInterval[1])
            else:
                if newInterval is not None and newInterval[1] < ivl[0]:
                    out.append(newInterval)
                    newInterval = None
                out.append(ivl)

        if newInterval is not None:
            out.append(newInterval)
            # if there isn't any overlap, append lastInterval
        #out.append(newInterval)
        return out

# name of the game: insert a new interval into a set of non-overlapping intervals,
# and make sure the resulting set of intervals do not overlap as well

# check for overlap. If there is any overlap, these intervals need to be merged
# and possibly create new merged interval from the current interval and the to-be
# merged interval
# if there is no overlap between the current interval, and the new interval,
# the current interval can be inserted without any trouble
# if the new interval comes before the current interval, insert the new
# interval, then the current interval. Setting the current interval to the "new interval"
# should make it so the logic works above, because the remaining intervals will
# be non-overlapping


