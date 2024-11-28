# 2024-11-28: the mathy-proofy solution is interested.
# also learned that gcd() is built in

import re
class Solution:
    # mathy-proofy solution
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ""

        max_length = gcd(len(str1), len(str2))
        return str1[:max_length]
    # brute force, based on editorial
    def gcdOfStringsV2(self, str1: str, str2: str) -> str:
        len1, len2 = len(str1), len(str2)

        def valid(k):
            if len1 % k or len2 % k:
                return False
            n1, n2 = len1 // k, len2 // k
            base = str1[:k]
            return str1 == n1 * base and str2 == n2 * base
            # using regex (from C++ solution)
            #return len(re.sub(base, '', str1)) == 0 and len(re.sub(base, '', str2)) == 0

        for i in range(min(len1, len2), 0, -1):
            if valid(i):
                return str1[:i]
        return ""
    # my hacked-up brute force solution
    def gcdOfStringsV1(self, str1: str, str2: str) -> str:
        # make sure str1 is larger or equal to str2
        if len(str1) < len(str2):
            tmp = str2
            str2 = str1
            str1 = tmp

        gcd = 0

        # brute force: try every combination
        print(len(str1), len(str2))

        for i in range(len(str2)):
            div = str2[:i+1]
            # if string doesn't evenly divide, it's
            # not going to work at all, so break early
            if len(str1) % len(div) != 0:
                continue

            if len(str2) % len(div) != 0:
                continue

            found = True
            for j in range(len(str1)):
                if str1[j] != div[j % len(div)]:
                    found = False
                    break
            if not found:
                continue

            # also check and make sure it works in divisor
            # TODO: this could be merged into a more elegant loop?
            found = True

            for j in range(len(str2)):
                if str2[j] != div[j % len(div)]:
                    found = False
                    break

            if found:
                gcd = i + 1


        return str2[:gcd]
