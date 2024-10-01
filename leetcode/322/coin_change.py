# WIP: NOT DONE

from pprint import pprint

# okay this isn't correct, but I'm trying to frame this
# in recursive terms
# say you have coins 0..N in sorted in ascending order
# the total number of coins can be represented as a sum
# of x_{n - 1} ... x_0 where
# x_{n - 1}*coins[n - 1] + x_{n - 2}*coins[n - 2] and so
# on equal exactly the target amount.
# You can find the exact amount of each by gradually peeling
# away larger currencies, which should be able to be
# found recursively.

# Try to see if 

def find_ncoins(coins, start, amount):
    if start < 0:
        return -1

    ncoins = amount // coins[start]

    if amount <= 0:
        return 0

    if ncoins * coins[start] == amount:
        return ncoins

    if ncoins == 1:
        return -1

    return (ncoins - 1) + find_ncoins(coins, start - 1, amount - coins[start])


def coin_change(coins, amount):
    if amount == 0:
        return 0
    total_coins = -1

    coins = sorted(coins, reverse=True)

    # start with the largest denomination of currency, which
    # will yield the smallest number of coins, then gradually
    # shift to the smaller coins to find a fit.
    # for c in coins:
    #     # assuming this is a floor divide, which means
    #     # amount will be less than or equal to amount
    #     ncoins = amount // c
    #     coin_amt = ncoins * c 
    #     if coin_amt == amount:
    #         # we are done, return number of coins
    #     elif coin_amt < amount:
    #         # attempt to find combination of remainder
    #         # from lower coins


    # return total_coins

rc = coin_change([1, 2, 5], 11)
assert(rc == 11)

rc = coin_change([2], 3)
assert(rc == -1)

rc = coin_change([1], 0)
assert(rc == 0)
