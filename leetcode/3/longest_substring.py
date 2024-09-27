# I worked out something which feels mostly right, but
# I have a hard time convincing myself that it is correct,
# even though the examples pass

# 2024-09-27: Revisiting this one since it showed up in
# Grind75. Checking the editorial to see what solutions
# they come up with.

# my initial attempt: use a hashmap to keep track of
# recurring characters.
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

# My second attempt at longest substring line of thinking
def longest_substr_v2(s):
    # hashmap, used to keep track of previous
    # indice positions
    h = {}
    maxsubstr = 1
    count = 0

    for i in range(0, len(s)):
        maxsubstr = max(count, maxsubstr)
        # a duplicate has been found
        if s[i] in h:
            count = 0
        h[s[i]] = i
        count += 1

    # okay, I don't love this last bit at the end for
    # the edgecase that all the characters are unique
    maxsubstr = max(count, maxsubstr)
    return maxsubstr

# check every possible combination, O(n^3) time
def longest_substr_naive(s):
    N = len(s)
    maxlen = 1
    for i in range(0, N):
        for k in range(0, N):
            substr = s[i:k+1]
            h = set(substr)
            if len(h) == len(substr):
                maxlen = max(maxlen, len(substr))

    return maxlen

def longest_substr_sliding_window(s):
    h = {}
    N = len(s)
    start = 0
    maxlen = 1

    for i in range(0, N):
        r = s[i]
        if r in h:
            h[r] += 1
        else:
            h[r] = 1

        while h[r] > 1:
            c = s[start]
            h[c] -= 1
            start += 1

        maxlen = max(maxlen, i - start + 1)

    return maxlen

# second approach from editorial.
def longest_substr_sliding_window_optimized(s):
    maxlen = 1
    N = len(s)
    h = {}

    lastpos = 0
    for i in range(0, N):
        if s[i] in h:
            lastpos = max(h[s[i]], lastpos)
        maxlen = max(maxlen, i - lastpos + 1)
        h[s[i]] = i + 1

    return maxlen

def test(f, run = True):
    out = f("abcabcbb")
    if run: assert(out == 3)

    out = f("bbbbb")
    if run: assert(out == 1)

    out = f("pwwkew")
    if run: assert(out == 3)

    # oops! this one breaks my initial implementation
    out = f("abcdef")
    if run: assert(out == 6)

# doesn't work!
test(longest_substr, False)
test(longest_substr_v2)
test(longest_substr_naive)
test(longest_substr_sliding_window)
test(longest_substr_sliding_window_optimized)
