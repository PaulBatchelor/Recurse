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
