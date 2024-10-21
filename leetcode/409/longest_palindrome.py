from collections import Counter
class Solution:
    def longestPalindrome(self, s: str) -> int:
        # a palindrome needs to evenly split character counts on each end
        # there can be one center node
        halfsize = 0
        counts = Counter(s)

        # the longest odd palindrome can go in the middle,
        # including 1-size counters, and can be kept track of
        # sizes greather than 2 can be appended to the size
        # if half the size is kept track of, then integer division
        # will allow 1-size items to be added, and also makes
        # computation of the final answer a little more slick (no conditional checks):
        # 2 * (halfsize - max_odd//2) + max_odd
        max_odd = 0
        for (k,c) in counts.items():
            if c % 2 == 1:
                max_odd = max(max_odd, c)
            # truncated divide gives the amount on one half,
            # times 2 gives the length
            halfsize += (c // 2)

        return (halfsize - (max_odd//2))*2 + max_odd
