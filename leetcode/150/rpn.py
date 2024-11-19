# 2024-11-19: I was very excited to do this one since
# I like stack-based languages. The thing that tripped
# me were the truncate-to-zero division rules, which
# were an issue whenever signed things were involved.
# (-6//132) goes to -1, while the asnwer should have been
# 0. I had an initial hack that extracts the sign, performs
# unsigned division, then re-introduces the sign, but it
# turns out that (int(x/y)) does the proper truncation
# behavior in Python. After looking at the editorial,
# I also did some refactoring and moved the pops out
# of each of the branches.

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stk = []

        for tk in tokens:
            if tk not in "+-/*":
                stk.append(int(tk))
                continue
            a = stk.pop()
            b = stk.pop()
            if tk == "+":
                stk.append(b + a)
            elif tk == "/":
                stk.append(int(b/a))
            elif tk == "*":
                stk.append(a * b)
            elif tk == "-":
                stk.append(b - a)

        return stk.pop()
