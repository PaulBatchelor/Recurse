# An attempt to transcribe the dynamic programming
# implementation of Skiena's string comparison problem,
# found on page 283

from pprint import pprint


def string_compare(s, t):

    # Skiena pads the strings with spaces to "keep matrix
    # m indeices in sync with those with the strings for
    # clarity"

    s = " " + s
    t = " " + t

    # don't use [[v]*n]*n, it's a trap!
    # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-list-of-lists-if-not-using-numpy-in
    #m  = [[None]*(len(t)+1)]*(len(s)+1)
    m  = [ [None]*(len(t)+1) for _ in range(len(s) + 1) ]

    # (i, 0) and (0, i) corresponding to matching length-i
    # strings against an empty string
    for i in range(0, len(m[0])):
        m[0][i] = i

    for i in range(0, len(m)):
        m[i][0] = i


    for i in range(1, len(s)):
        for j in range(1, len(t)):
            match = m[i - 1][j - 1]

            if s[i] != t[j]:
                match += 1

            insert = m[i][j - 1] + 1
            delete = m[i - 1][j] + 1

            m[i][j] = min(match, insert, delete)

    i = len(s) - 1
    j = len(t) - 1

    return m[i][j]

out = string_compare("thou shalt not", "you should not")
print(out)
