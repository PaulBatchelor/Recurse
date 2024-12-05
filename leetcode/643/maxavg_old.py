# one of the solutions in the editorial (sliding window)
# 2024-08-13: 00:31:39
def sliding_window(nums, k):
    sum = 0
    for i in range(0, k):
        sum += nums[i]

    res = sum
    
    for i in range(k, len(nums)):
        #sum += nums[i] - nums[i - k]
        sum += nums[i]
        sum -= nums[i - k]
        res = max(res, sum)

    return res / k

# My initial brute-force solution
def brute_force(nums, k):
    maxsum = None
    for i in range(k, len(nums)):
        sum = 0
        for j in range(0, k):
            sum += nums[(i - k) + j]

        sum /= k
        if maxsum == None:
            maxsum = sum
        else:
            maxsum = max(maxsum, sum)
    return maxsum

# cumulative sum (editorial)
def cumsum(nums, k):
    csum = []
    csum.append(nums[0])
    for i in range(1, len(nums)):
        csum.append(csum[i - 1] + nums[i])

    res = csum[k - 1] / k;

    # in:  1 2 3 4  5  6
    # out: 1 3 6 10 16 21

    # out[4] - out[1] =
    # (1 + 2 + 3 + 4 + 5) -
    # (1 + 2)
    # 16 - 3 = 13

    for i in range(k, len(nums)):
        res = max(res, (csum[i] - csum[i - k]) / k)

    return res

avg = sliding_window([1, 12, -5, -6, 50, 3], 4)
assert(avg == 12.75)

avg = brute_force([1, 12, -5, -6, 50, 3], 4)
assert(avg == 12.75)

avg = cumsum([1, 12, -5, -6, 50, 3], 4)
assert(avg == 12.75)
