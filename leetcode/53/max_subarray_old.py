# botched attempt at 2-pointer
def max_subarray(nums):
    total = 0
    left = 0
    right = len(nums) - 1
    last_left = left
    last_right = right

    for v in nums:
        total += v

    while (left < right):
        if (total - nums[last_left + 1]) > total:
            total -= nums[last_left + 1]
            last_left += 1
        if (total - nums[last_right - 1]) > total:
            total -= nums[last_right - 1]
            last_right -= 1

        left += 1
        right -= 1
    print(total, last_left, last_right)
    return total

# okay *this* is a two-pointer sliding window
def max_subarray_v2(nums):
    total = 0
    left = 0
    right = len(nums) - 1

    for v in nums:
        total += v
    max_total = total

    while (left < right):
        total -= nums[left]
        max_total = max(total, max_total)
        total -= nums[right]
        max_total = max(total, max_total)
        left += 1
        right -= 1

    return max_total

def test(f):
    rc = f([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert(rc == 6)

    rc = f([1])
    assert(rc == 1)

    rc = f([5, 4, -1, 7, 8])
    assert(rc == 23)

test(max_subarray_v2)
