from pprint import pprint


# actually I think this is the brute force solution
# actually I also think this could be false logic,
# the max() thing is just something I felt would work
# here, but I didn't rigorously prove it like how they
# work out this solution in the book
def lcs(t1, t2):
    m = len(t1)
    n = len(t2)
    maxsubstr = 0

    p = [[0]*n for _ in range(m)]

    if t1[0] == t2[0]:
        for j in range(n):
            p[0][j] = 1
    for i in range(1, m):
        for j in range(n):
            p[i][j] = max(maxsubstr, p[i - 1][j])
            if t1[i] == t2[j]:
                p[i][j] += 1
            maxsubstr = max(maxsubstr, p[i][j])

    return maxsubstr

# TODO transcribe the textbook solution to thistranscribe the textbook solution to this

out = lcs("ace", "abcde")
assert (out == 3)

out = lcs("abc", "abc")
assert (out == 3)

out = lcs("abc", "def")
assert (out == 0)
