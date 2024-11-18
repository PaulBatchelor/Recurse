# 2024-11-18: My solution (v1) was something I recalled
# pretty quickly. The other versions are from the editorial

from collections import Counter
class Solution:
    # approach 3: sliding window optimized
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        ans = 0

        charToNextIndex = {}

        i = 0

        for j in range(n):
            if s[j] in charToNextIndex:
                i = max(charToNextIndex[s[j]], i)

            ans = max(ans, j - i + 1)
            charToNextIndex[s[j]] = j + 1

        return ans

    # approach 2: sliding window using hashset
    def lengthOfLongestSubstringv3(self, s: str) -> int:
        chars = Counter()
        left = right = 0

        res = 0
        while right < len(s):
            r = s[right]
            chars[r] += 1
            while chars[r] > 1:
                l = s[left]
                chars[l] -= 1
                left += 1

            res = max(res, right-left + 1)
            right += 1

        return res

    # my solution: keep track of positions and update
    def lengthOfLongestSubstringv1(self, s: str) -> int:
        if len(s) == 0:
            return 0
        maxlen = 1
        positions = {}
        left = 0
        for i,ch in enumerate(s):
            if ch in positions and positions[ch] >= left:
                left = positions[ch] + 1
            positions[ch] = i
            maxlen = max(maxlen, i - left + 1)

        return maxlen
