from pprint import pprint

phone_letters = [
    None, None,
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i'],
    ['j', 'k', 'l'],
    ['m', 'n', 'o'],
    ['p', 'q', 'r'],
]

# digits = "23"

# pprint(phone_letters[int(digits[0])])

def backtrack(A, k, digits, results):
    k += 1
    if k == len(digits):
        results.append(''.join(A[0:k]))
        return
    candidates = phone_letters[int(digits[k])]
    for i in range(0, len(candidates)):
        A[k] = candidates[i]
        backtrack(A, k, digits, results)

def letter_combo(digits):
    results = []
    if len(digits) == 0:
        return []

    A = [None]*len(digits)
    backtrack(A, -1, digits, results)
    return results


out = letter_combo("23")
pprint(out)

out = letter_combo("")
pprint(out)

out = letter_combo("2")
pprint(out)
