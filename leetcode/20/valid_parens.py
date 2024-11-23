# 2024-11-23: This one I almost got right on the first go
# except for the edge case where there'd be too many opens
# I missed this the last time I attempted this, but didn't
# catch it since I didn't submit it
class Solution:
    def isValid(self, s: str) -> bool:
        # length of string must be multiple of 2 to be valid
        if len(s) % 2 == 1:
            return False

        stk = []

        # linear sweep through string
        for p in s:
            if p in "([{":
                stk.append(p)
                continue
            # attmpt to see if closing paren matches
            if len(stk) == 0:
                return False

            open_paren = stk.pop()

            if open_paren == "(" and p == ")":
                continue
            elif open_paren == "{" and p == "}":
                continue
            elif open_paren == "[" and p == "]":
                continue
            else:
                return False

        # non-zero items on the stack implies it is unbalanced
        return len(stk) == 0

# old non-LC version

def valid_parens(s):
    stack = []
    lparens = {'{', '[', '('}
    for n in range(0, len(s)):
        if s[n] in lparens:
            stack.append(s[n])
        else:
            if len(stack) == 0:
                return False
            p = stack[-1]
            matching = \
                p == '{' and s[n] == '}' or \
                p == '(' and s[n] == ')' or \
                p == '[' and s[n] == ']'
            if matching:
                stack.pop()
            else:
                return False
    return True

rc = valid_parens("()")
assert(rc)
rc = valid_parens("()[]{}")
assert(rc)
rc = valid_parens("(]")
assert(not rc)
rc = valid_parens("([])")
assert(rc)
