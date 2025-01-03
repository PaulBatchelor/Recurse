# 2025-01-03: Figured out bruteforce quickly O(n*log(n)), somehow
# managed to work out the O(n) logic from looking at patterns
# and gaining an intution about 0 LSB.
class Solution:
    def countBits(self, n: int) -> List[int]:
        out = [0]*(n + 1)

        for num in range(1, n + 1):
            prev = num - 1

            if prev & 1:
                out[num] = out[(prev - 1) & num] + 1
            else:
                out[num] = out[prev] + 1

        return out
    def countBits_bruteforce(self, n: int) -> List[int]:
        def count(n):
            out = 0
            while n:
                if n & 1:
                    out += 1
                n >>= 1
            return out

        out = [0]*(n + 1)
        for num in range(1,n + 1):
            out[num] = count(num)
        return out

# 000
# 001
# 010
# 011
# 100

# 010
# 011
# 100

# 1100
# 1101
# 1110

# 000 0
# 001 1
# 010 1
# 011 2
# 100
# 101
