# 2024-11-24: two-pointer solution, with compare with
# filtered reverse string approach
class Solution:
    def isPalindrome_reversed(self, s: str) -> bool:
        filtered_chars = filter(lambda ch: ch.isalnum(), s)
        lowercase_filtered_chars = map(lambda ch: ch.lower(), filtered_chars)
        filtered_chars_list = list(lowercase_filtered_chars)
        reversed_chars_list = filtered_chars_list[::-1]

        return filtered_chars_list == reversed_chars_list
    # my version, conventional two-pointer wisdom
    def isPalindrome(self, s: str) -> bool:
        # convert to lowercase for case insensitivity
        s = s.lower()

        left = 0
        right = len(s) - 1

        while left < right:
            # check if left/right characters are non-alphanumeric, and move
            # the pointers

            if not (s[left].isalpha() or s[left].isnumeric()):
                left += 1
                continue
            if not (s[right].isalpha() or s[right].isnumeric()):
                right -= 1
                continue

            # at this point, ends are alphanumeric characters, check and see if
            # they match. If they don't, it is not a palindrome

            if s[left] != s[right]:
                return False

            # pairs match, move both pointers
            left += 1
            right -= 1
        return True

# Valid palindrome: the intuitive way to do this is to
# sweep through the string and check the beginnings/endings
# to ensure they match. Python has built-in ways to remove
# no alphanumeric characters, which will simplify the
# code logic tremendously. Short of that, one would need
# adopt a sort of two pointer solution that reads the string
# in place.

import re

# v1: pre-process string before checking
def valid_palindrome_v1(str):
    str = re.sub("[^a-z]+", "", str.lower())
    N = len(str)

    for i in range(0, N//2):
        s1 = str[i]
        s2 = str[N - i - 1]
        if s1 != s2:
            return False

    return True

# v2: two-pointer. check the string in place
def valid_palindrome_v2(str):
    left = 0
    right = len(str) - 1

    while(left < right):
        if not str[left].isalpha():
            left += 1
            continue
        elif not str[right].isalpha():
            right -= 1
            continue
        else:
            if str[right].lower() != str[left].lower():
                return False
            left += 1
            right -= 1

    return True


def test(f):
    rc = f("A man, a plan, a canal: Panama")
    assert(rc)
    
    rc = f("race a car")
    assert(not rc)
    
    rc = f(" ")
    assert(rc)

test(valid_palindrome_v1)
test(valid_palindrome_v2)
