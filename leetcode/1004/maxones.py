# This one does NOT work at all. It is completely
# broken and incorrect.
def attempt(nums, k):
    L = 0
    count = 0
    start = 0

    if nums[0] == 0:
        count += 1

    maxlen = 0

    for i in range(1, len(nums)):
        if nums[i] == 0:
            if count == k:
                count -= 1
                start = L + 1
                
                for x in range(start, len(nums)):
                    if nums[x] == 0:
                        L = x
                        break;

        maxlen = max(maxlen, i - start)
    return maxlen


# currently incorrect, even though it's allegedly ported
# from the C++ answer
def editorial(nums, k):
    L = 0
    for R in range(0, len(nums)):
        if nums[R] == 0:
            k -= 1
        if k < 0:
            k += 1 - nums[L]
            L += 1
    return R - L

nums = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
k = 3

out = attempt(nums, k)
assert(out == 10)

# out = editorial(nums, k)
# assert(out == 10)
