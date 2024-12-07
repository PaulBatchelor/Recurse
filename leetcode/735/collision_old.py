def collision(asteroids):
    stack = []
    for ast in asteroids:
        stack.append(ast)
        while(1):
            if len(stack) < 2:
                break

            a1 = stack.pop()
            a2 = stack.pop()

            a1dir = a1 < 0
            a2dir = a2 < 0

            if (a1dir == a2dir):
                stack.append(a2)
                stack.append(a1)
                break
            else:
                if abs(a2) != abs(a1):
                    largest = None
                    if abs(a2) > abs(a1):
                        largest = a2
                    else:
                        largest = a1
                    stack.append(largest)
    return stack

out = collision([5, 10, -5])
assert(out == [5, 10])

out = collision([8, -8])
assert(out == [])

out = collision([10, 2, -5])
assert(out == [10])
