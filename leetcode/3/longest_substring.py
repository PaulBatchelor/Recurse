# I worked out something which feels mostly right, but
# I have a hard time convincing myself that it is correct,
# even though the examples pass

def longest_substr(s):
    start = 0
    h = {}
    max = 1
    N = len(s)

    for i in range(0, N):
        if s[i] in h:
            new_max = i - start
            if new_max > max:
                max = new_max
            start = h[s[i]] + 1
        h[s[i]] = i

    return max

out = longest_substr("abcabcbb")
assert(out == 3)

out = longest_substr("bbbbb")
assert(out == 1)

out = longest_substr("pwwkew")
assert(out == 3)
