# 2024-11-25 My revisited version. Turns out I did this
# already oops

# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n
        while left < right:
            mid = left + (right - left) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1
        return left

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
