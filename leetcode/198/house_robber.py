def house_robber(nums):
    c0 = nums[0]
    c1 = nums[1]
    c2 = nums[2] + c0
    c3 = max(c0, c1) + nums[3]

    for i in range(4, len(nums)):
        c0 = c1
        c1 = c2
        c2 = c3
        c3 = max(c0, c1) + nums[i]
        

    return max(c3, c2)

out = house_robber([1, 2, 3, 1])
assert(out == 4)

out = house_robber([2, 7, 9, 3, 1])
assert(out == 12)

out = house_robber([2, 7, 9, 3, 1, 1, 1, 5, 2, 6])
assert(out == 23)

