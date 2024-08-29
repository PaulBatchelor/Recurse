from pprint import pprint

def backtrack(A, k, n, results):
    if len(A) < k and sum(A) >= n:
        return

    if len(A) == k:
        if sum(A) == n:
            results.append(A[0:k])
        return

    last = 1

    if len(A) > 0:
        last = A[-1] + 1
    for i in range(last, 10):
        A.append(i)
        backtrack(A, k, n, results)
        A.pop()


def csum3(k, n):
    results = []
    A = []
    backtrack(A, k, n, results)
    return results

out = csum3(3, 7)
pprint(out)

out = csum3(3, 9)
pprint(out)

out = csum3(4, 1)
pprint(out)
