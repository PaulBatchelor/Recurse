def stock_max_profit(prices):
    left = 0
    right = len(prices) - 1
    min_val = prices[left]
    max_val = prices[right]

    while left < right:
        lval = prices[left]
        rval = prices[right]

        if lval < min_val:
            min_val = lval

        if rval > max_val:
            max_val = rval

        left += 1
        right -= 1

    max_profit = max_val - min_val

    if max_profit < 0:
        return 0

    return max_profit

out = stock_max_profit([7, 1, 5, 3, 6, 4])
assert(out == 5)

out = stock_max_profit([7, 6, 3, 1])
assert(out == 0)
