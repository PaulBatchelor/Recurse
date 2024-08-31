from pprint import pprint


# actually I think this is the brute force solution
# actually I also think this could be false logic,
# the max() thing is just something I felt would work
# here, but I didn't rigorously prove it like how they
# work out this solution in the book
# EDIT: yup, this is a broken implementation, it breaks
# on the input example found in the book.
def lcs_v1(t1, t2):
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

# this is the version transcribed from the textbook implementation
# found in CLRS, page 394

def lcs_v2(t1, t2):
    m = len(t1)
    n = len(t2)
    c = [[0]*(n + 1) for _ in range((m + 1))]

    for i in range(m + 1):
        c[i][0] = 0

    for j in range(n + 1):
        c[0][j] = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if t1[i - 1] == t2[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
            else:
                c[i][j] = c[i][j - 1]

    return c[m][n]

def lcs(t1, t2):
    return lcs_v2(t1, t2)

out = lcs("ABCBDAB", "BDCABA")
assert (out == 4)

out = lcs("ace", "abcde")
assert (out == 3)

out = lcs("abc", "abc")
assert (out == 3)

out = lcs("abc", "def")
assert (out == 0)
