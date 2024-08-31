def unique_paths(n, m):
    p = [[0] * m for _ in range(n)]

    for j in range(1, m):
        p[0][j] = 1

    for i in range(1, n):
        p[i][0] = 1

    for i in range(1, n):
        for j in range(1, m):
            p[i][j] = p[i - 1][j] + p[i][j - 1]

    return p[n - 1][m - 1]

out = unique_paths(3, 7)
assert(out == 28)

out = unique_paths(3, 2)
assert(out == 3)

