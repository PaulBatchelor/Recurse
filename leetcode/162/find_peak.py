from pprint import pprint
# I almost got the linear time implementation correct,
# except I didn't realize that the ends could be peaks
# as well.
# The recursive binary search solution is something I
# am skeptical of, so I'm implementing it to see if it
# actually works. And if it does, I'm going to try to better
# grok why it works the way it does.

def search(nums, start, end):
    pprint(nums[start:end + 1])
    # bounds have converged on an index
    if start == end:
        return start

    mid = (start + end) // 2
    # this seems to be equivalent (how I've computed
    # midpoints previously):
    # mid = start + (end - start)//2

    if nums[mid] > nums[mid + 1]:
        return search(nums, start, mid)

    return search(nums, mid + 1, end)

def find_peak(nums):
    return search(nums, 0, len(nums) - 1)

out = find_peak([1, 2, 3, 1])
assert(out == 2)

out = find_peak([1, 2, 1, 3, 5, 6, 4])
assert(out == 5)

# this answer returns a 
out = find_peak([1, 2, 1, 3, 5, 6, 4])
print(out)
