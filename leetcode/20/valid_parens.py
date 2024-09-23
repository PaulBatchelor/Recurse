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
            if p == '{' and s[n] == '}':
                stack.pop()
            elif p == '(' and s[n] == ')':
                stack.pop()
            elif p == '[' and s[n] == ']':
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
