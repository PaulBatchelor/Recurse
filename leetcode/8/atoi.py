# 2024-10-25: Leveraged python mechanisms a bit for brevity and speed
# missed many of the edge cases. tricky.
class Solution:
    def myAtoi(self, s: str) -> int:
        out = 0
        s = s.lstrip(" ")
        if len(s) == 0:
            return 0

        # determine sign
        sign = 1
        if s[0] == "-":
            sign = -1
            s = s[1:]
        elif s[0] == "+":
            sign = 1
            s = s[1:]

        num = []
        for c in s:
            if not c.isnumeric():
                break
            num.append(c)
        if len(num) == 0:
            return 0
        num = "".join(num)
        num = int(num) * sign

        # round to be in bounds [-2^32, 2^32]
        num = max(-2**31, num)
        num = min(2**31 - 1, num)
        return num
