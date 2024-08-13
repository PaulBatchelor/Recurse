# Just double checking here. The editorial had an
# implicit "rsum", possibly to shave off an operation
# I am going to check and see if what I wrote down is
# equivalent using both rsum and lsum.

def find_pivot(nums):
    lsum = 0
    rsum = 0

    for x in nums:
        rsum += x

    for i in range(0, len(nums)):
        if lsum == rsum - nums[i]:
            return i
        lsum += nums[i]
        rsum -= nums[i]

    return -1

nums = [1, 7, 3, 6, 5, 6]

out = find_pivot(nums)

assert(out == 3)
