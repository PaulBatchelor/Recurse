#2024-10-24: after a few attempts at elegance, I came up with
# a very slow brute-force solution

class Solution:
    def isPalindrome(self, s, start, end):
        #print(f"Testing {s[start:end + 1]}")
        while start < end:
            if s[start] != s[end]:
                return False
            start += 1
            end -= 1

        #print(f"{start}, {end} is palindrome")

        return True

    def longestPalindrome(self, s:str) -> str:
        N = len(s)
        #cursize = N

        for cursize in range(N, 0, -1):
            for end in range(cursize - 1, N):
                start = end - cursize + 1
                #print(cursize, start, end)
                if self.isPalindrome(s, start, end):
                    return s[start:end+1]
        return s[0]
    # lops off values too early
    def longestPalindromeV2(self, s: str) -> str:
        left = 0
        right = len(s) - 1
        while left < right:
            if self.isPalindrome(s, left, right):
                return s[left:right + 1]
            elif self.isPalindrome(s, left + 1, right):
                return s[left + 1:right + 1]
            elif self.isPalindrome(s, left, right - 1):
                return s[left:right]

            left += 1
            right -= 1
        
        return s
    
    # wrong: last_seen heuristic discards potential palindromes because
    # movement is left->right
    def longestPalindromeV1(self, s: str) -> str:
        last_seen = {}
        maxsize = 1
        maxrange = [0, 0]
        
        for i in range(0, len(s)):
            c = s[i]
            if c in last_seen:
                # TODO: speed things up by skipping palindrome check
                # if distance is smaller than max range
                if not self.isPalindrome(s, last_seen[c], i):
                    # impossible for later chars to be palindrome
                    last_seen[c] = i
                else:
                    dist = i - last_seen[c] + 1
                    if dist > maxsize:
                        maxrange = [last_seen[c], i]
                        maxsize = dist
            else:
                last_seen[c] = i

        return s[maxrange[0]:maxrange[1] + 1]


# feels two-pointer-ish
# cast a net with the largest possible substring (all of it), and work inwards
# find the largest "bookends" and check to see if that range is a palindrome
# if not keep shrinking

# how to ensure that largest values aren't missed?
# maybe a hashmap? Store an index of the rightmost values of every character
# then, sweep left to right. if the distance between the two indices is greater than
# the current max, check to see if range is palindrome. if it is, store a new max value,
# as well as the range

# rightmost doesn't work either, it's not guaranteed that the rightmost value is going
# to be a palindrome

# another idea: left to right, keep track of last seen index for a given character
# check for palindromes that way

# solution ran into edgecase: my logic moving left to right makes the false assumption
# that if a palindrome for a given ragne doesn't work, then the last seen is updated
# with the rightmost found index so far. But, this can miss bigger palindromes (such as
# those that encapsulate the whole string).

# how do we start large, and iteratively prove that it's not a palindrome?
# if characters can be popped off ends, then that substring needs to be proven
# that it is or isn't a palindrome.
# the first palindrome found this way is going to be largest

# abadd is not a palindrome, a != d
# abad and badd isn't a palindrome, a != d and b != d
# aba is a palindrome, a == a, bad isn't a palindrome b != d

# My peeling strategy doesn't work because it lops of letters too soon

# more brute force approach: start with the largest possible range
