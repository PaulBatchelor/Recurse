def binary_search(nums, target):
    start = 0
    end = len(nums) - 1

    while start <= end:
        mid = start + ((end - start) // 2)
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            start = mid + 1
        elif nums[mid] > target:
            end = mid - 1

    return -1

rc = binary_search([-1, 0, 3, 5, 9, 12], 9)
assert(rc == 4)

rc = binary_search([-1, 0, 3, 5, 9, 12], 12)
assert(rc == 5)

rc = binary_search([-1, 0, 3, 5, 9, 12], -1)
assert(rc == 0)

rc = binary_search([-1, 0, 3, 5, 9, 12], 2)
assert(rc == -1)
