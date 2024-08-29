# transcribed from C/C++ code in skiena example, pg 280

from pprint import pprint

def binomial(n, m):
    bc = []

    for i in range(0, n+1):
        bc.append([0]*(n + 1))

    for i in range(0, n + 1):
        bc[i][0] = 1

    for j in range(0, n + 1):
        bc[j][j] = 1

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            bc[i][j] = bc[i - 1][j - 1] + bc[i - 1][j]

    pprint(bc)

    return bc[n][m]

out = binomial(5, 4)

print(out)
