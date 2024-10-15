# 10/11 My first solution was a little more verbose
# than this, with unnecessary checks. I fed it through
# claude, and it gave me the more optimal approach here:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        # divide and conquer
        start = 1
        end = n
        while start < end:
            mid = start + (end - start) // 2
            if isBadVersion(mid):
                end  = mid
            else:
                start = mid + 1
        return start
