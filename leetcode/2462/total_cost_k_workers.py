# My solution feels inefficient, but correct. Going to
# implement this to see if I'm missing anything, then
# I'll check the answer. This is supposed to be a heap
# problem, so I get the feeling that I'm missing something
# in my approach because mine is essentially brute force

def brute_force(costs, candidates, k):
    k = min(k, len(costs))
    sum = 0
    N = len(costs)

    for c in range(0, candidates):
        min_left = costs[0]
        min_left_idx = 0

        min_right = costs[len(costs) - 1]
        min_right_idx = len(costs) - 1
        for i in range(0, k):
            lpos = i
            rpos = N - 1 - i

            lval = costs[lpos]
            rval = costs[rpos]

            if lval < min_left:
                min_left = lval
                min_left_idx = lpos

            if rval < min_right:
                min_right = rval
                min_right_idx = rpos

   
        selidx = min_left_idx
        if min_right == min_left:
            selidx = min_left_idx
        if min_right < min_left:
            selidx = min_right_idx
       
        val = costs.pop(selidx)
        sum += val
        N = len(costs)
        k = min(k, N)

    return sum

out = brute_force([17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4)
assert(out == 11)

out = brute_force([1, 2, 4, 1], 3, 3)
assert(out == 4)
