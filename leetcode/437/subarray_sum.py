# the subproblem of this binary tree problem is the
# subarray sum. I am trying to understand how the solution
# works.
from pprint import pprint
from collections import OrderedDict

def subarray_sum(arr, target):
    counts = OrderedDict()
    # created prefix sum and place in hashmap
    psum = []
    ncounts = 0
    instr = []

    psum.append(arr[0])
    counts[psum[0]] = 1

    for i in range(1, len(arr)):
        sum = psum[i - 1] + arr[i]
        #counts[sum] = 1
        counts[sum] = counts.get(sum, 0) + 1
        psum.append(sum)

    for i in range(0, len(arr)):
        cursum = psum[i]
        if cursum == target:
            instr.append(f"{i}:C==T")
            ncounts += 1

        if (cursum - target) in counts:
            instr.append(f"{i}:NC+={counts.get(cursum - target)}")
            ncounts += counts[cursum - target]

    pprint(counts)
    pprint(instr)
    return ncounts

# follows more closely the coded solution, which does
# it in one pass and only the hashmap
def subarray_sum2(nums, target):
    h = OrderedDict()
    cursum = 0
    ncounts = 0 

    for i in range(0, len(nums)):
        cursum += nums[i]
        if cursum == target:
            ncounts += 1

        ncounts += h.get(cursum - target, 0)
        h[cursum] = h.get(cursum, 0) + 1

    return ncounts

def subarray_sum3(nums, target):
    h = OrderedDict()
    cursum = 0
    ncounts = 0 
    instr = []

    for i in range(0, len(nums)):
        cursum += nums[i]
        if cursum == target:
            instr.append(f"{i}:C==T")
            ncounts += 1

        if cursum - target in h:
            instr.append(f"{i}:NC+={h.get(cursum - target)}")
            ncounts += h.get(cursum - target, 0)
        h[cursum] = h.get(cursum, 0) + 1

    pprint(h)
    pprint(instr)
    return ncounts


# out = subarray_sum2([3, 4, 1, 6, -3], 7)
# print(out)
# assert(out == 2)

# dictionary required because negative numbers could
# cause prefix sums to occur multiple times like below
out = subarray_sum([3, 4, -7, 1, 6, -3], 7)
out = subarray_sum2([3, 4, -7, 1, 6, -3], 7)
print(out)
#assert(out == 3)

# why do we increment using hashmap count?
out = subarray_sum2([3, 4, 1, 6, -3, -11, 3, 4, 1, 6], 7)
print(out)
