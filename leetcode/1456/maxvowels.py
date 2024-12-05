# 2024-12-05: sliding window from memory, worked on
# iterating on the code a little bit. Learned that int()
# can coerce boolean values

class Solution:
    # value coercion for boolean values
    def maxVowels(self, s: str, k: int) -> int:
        maxvows = 0
        vowcount = 0
        for i in range(len(s)):
            if i >= k:
                vowcount -= int(s[i - k] in "aeiou")
            vowcount += int(s[i] in "aeiou")
            maxvows = max(maxvows, vowcount)

        return maxvows
    # do it all in one loop
    def maxVowelsV2(self, s: str, k: int) -> int:
        maxvows = 0
        vowcount = 0
        for i in range(len(s)):
            if i >= k and s[i - k] in "aeiou":
                vowcount -= 1
            if s[i] in "aeiou":
                vowcount += 1
            maxvows = max(maxvows, vowcount)

        return maxvows

    def maxVowelsV1(self, s: str, k: int) -> int:
        maxvows = 0

        for i in range(k):
            if s[i] in "aeiou":
                maxvows += 1
        vowcount = maxvows
        for i in range(k, len(s)):
            if s[i - k] in "aeiou":
                vowcount -= 1
            if s[i] in "aeiou":
                vowcount += 1

            maxvows = max(maxvows, vowcount)

        return maxvows
