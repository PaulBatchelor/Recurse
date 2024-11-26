# 2024-11-26: I worked out the conventional solution that
# works fine, though it's unrefined. The editorial
# solution for the same thing is my pythonic and uses
# more built-in methods. There was a very slick bitwise
# manipulation solution which I have also included.

class Solution:

    # Approach 2: bitwsie manipulation
    def addBinary(self, a: str, b: str) -> str:
        x, y = int(a, 2), int(b, 2)
        while y:
            answer = x ^ y
            carry = (x & y) << 1
            x, y = answer, carry
        return bin(x)[2:]
    # Approach 1: bit-by-bit computation, a bit cleaner than my solution
    def addBinaryV2(self, a: str, b: str) -> str:
        n = max(len(a), len(b))
        a, b = a.zfill(n), b.zfill(n)

        carry = 0
        answer = []

        for i in reversed(range(n)):
            if a[i] == "1":
                carry += 1
            if b[i] == "1":
                carry += 1

            if carry % 2 == 1:
                answer.append("1")
            else:
                answer.append("0")

            carry >>= 1

        if carry == 1:
            answer.append("1")
        answer.reverse()

        return "".join(answer)

    # my unrefined working solution
    def addBinaryV1(self, a: str, b: str) -> str:
        carry = False
        out = []
        a = list(a)
        b = list(b)
        while(a and b):
            x = int(a.pop())
            y = int(b.pop())
            res = "0"
            if carry:
                carry = False
                # 0 0 => 1, False
                # 1 0 => 0, True
                # 1 1 => 1, True

                if x ^ y:
                    carry = True
                elif x == y:
                    res = "1"
                    if x == 1:
                        carry = True
            elif x & y:
                carry = True
            elif x ^ y:
                res = "1"
            out.append(res)

        remain = a or b

        while remain:
            x = int(remain.pop())
            res = str(x)
            if carry:
                res = "0"
                carry = False
                if x == 1:
                    carry = True
                else:
                    res = "1"
            out.append(res)

        if carry:
            out.append("1")
        out.reverse()
        return "".join(out)


# 1010
# 1011
# -----
# 10101

# 11
# 11
# --
# 110
