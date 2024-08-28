# I immediately understood the concept, but I got the
# details wrong on this one in my handwritten implementation.
# going to implement a working version just to get it in
# in my fingers. This will be silly, because the guess
# will be part of the function

def guess(n, pick):
    if n > pick:
        return -1
    elif n < pick:
        return 1

    return 0

def guessgame(n, pick):
    low = 1
    high = n

    while low <= high:
        mid = low + (high - low)//2
        res = guess(mid, pick)

        if res == 0:
            return mid
        elif res < 0:
            high = mid - 1
        else:
            low = mid + 1

    return -1


out = guessgame(10, 3)
assert(out == 3)
