def maxvowels(s, k):
    maxv = 0
    vowels = {'a', 'e', 'i', 'o', 'u'}
    count = 0

    # part 1: intialize sliding window for first k values
    for i in range(k):
        if s[i] in vowels:
            count += 1
    maxv = count

    # part 2: sweep through the string up to N - k.
    for i in range(k, len(s)):
        if s[i - k] in vowels:
            count -= 1
        if s[i] in vowels:
            count += 1
        maxv = max(count, maxv)
    return maxv

out = maxvowels("abciiidef", 3)
assert(out == 3)

out = maxvowels("aeiou", 2)
assert(out == 2)

out = maxvowels("leetcode", 3)
assert(out == 2)

