from pprint import pprint

# fewest number of coins: use larger denominations
# find the combination with the maximum number of large
# denominations
#
# first find the combination, then add up the number
# ncoins(coin_n, amount) +
# ncoins(coin_{n - 1}, amount - ncoins(coin_n, amount)*coin_n) +
# ncoins(coin_{n - 2}, amount - ncoins(coin_{n - 1}, amount)*coin_{n - 1}) +

# this is the recursive solution, it probably should
# be memoized somehow to make it a dynamic programming problem

def ncoins(coins, coin_idx, amount, count):
    if amount == 0:
        return count

    if coin_idx == len(coins):
        return -1

    max_coins = amount // coins[coin_idx]

    if max_coins == 0:
        return ncoins(coins, coin_idx + 1, amount, count)

    if (max_coins * coins[coin_idx]) == amount:
        print(f"found {max_coins} of {coins[coin_idx]} equals {amount}")
        return count + max_coins

    for i in range(max_coins, 0, -1):
        print(f"trying {i} of {coins[coin_idx]}")
        total = i * coins[coin_idx]
        newcount = ncoins(coins, coin_idx + 1, amount - total, count + i)
        if newcount > 0:
            return newcount

    return -1

def coin_change(coins, amount):
    coins = sorted(coins, reverse=True)
    x = ncoins(coins, 0, amount, 0)
    print(x)
    return x

rc = coin_change([1, 2, 5], 11)
assert(rc == 3)

rc = coin_change([2], 3)
assert(rc == -1)

rc = coin_change([1], 0)
assert(rc == 0)
