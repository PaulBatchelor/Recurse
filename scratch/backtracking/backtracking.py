# backtracking code, adapted from C++ to python from
# Skiena

from pprint import pprint

finished = False

def make_move(a, k, input):
    pass

def unmake_move(a, k, input):
    pass

def construct_candidates(a, k, input):
    return [True, False]

def process_solution(a, k, input):
    outstr = "{"
    for i in range(1, k+1):
        if a[i]: outstr += f" {i}"

    outstr += " }"

    print(outstr)

def is_a_solution(a, k, n):
    return k == n

def backtrack(a, k, input):
    if is_a_solution(a, k, input):
        process_solution(a, k, input)
    else:
        k += 1
        c = construct_candidates(a, k, input)
        for i in range(0, len(c)):
            a[k] = c[i]
            make_move(a, k, input)
            backtrack(a, k, input)
            unmake_move(a, k, input)
            if (finished): return


def generate_subsets(n):
    a = [0]*(n + 1)

    backtrack(a, 0, n)


generate_subsets(3)
