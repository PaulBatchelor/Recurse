from pprint import pprint
# once again comparing my approach with the solution
# the solution in the editorial makes use of a stack,
# but mine uses recursion. Do both work?

def use_stack(rooms):
    stack = []
    visited = [False] * len(rooms)
    stack.append(0)
    visited[0] = True

    while len(stack) > 0:
        node = rooms[stack.pop()]
        for m in node:
            if not visited[m]:
                visited[m] = True
                stack.append(m)

    for v in visited:
        if not v:
            return False

    return True

def visit(rooms, node, visited):
    for m in rooms[node]:
        if not visited[m]:
            visited[m] = True
            visit(rooms, m, visited)

def use_recursion(rooms):
    visited = [False] * len(rooms)
    visited[0] = True
    visit(rooms, 0, visited)
    for v in visited:
        if not v:
            return False
    return True

rooms = [[1], [2], [3], []]
visited = use_stack(rooms)
assert(visited == True)
visited = use_recursion(rooms)
assert(visited == True)

rooms = [[1, 3], [3, 0, 1], [2], [0]]
visited = use_stack(rooms)
assert(visited == False)
visited = use_recursion(rooms)
assert(visited == False)
