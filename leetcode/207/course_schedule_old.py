# Some intuition:
# - The structure here is a dependency graph (aka a DAG)
# - Depth-First traversal. Can you traverse N nodes?
# - It's a cycles check which a topological sort can check,
# - but hopefully DFS by itself can solve this?

from pprint import pprint

# 2024-10-01. I don't have this one yet.
# I know there needs to be traversal, and it should be
# depth-first. The number of unique nodes visited should
# equal to the number of courses.

# follow-up: I did an initial step where I found all
# the nodes without prereqs, then iterated through
# those depth-first using a stack, and using a set to
# keep track of nodes. Processed is used to keep track
# of cycles

def course_schedule(ncourses, prerequisites):
    processed = set()
    edges = prerequisites

    stk = []

    # [A, B] means course B needs to be taken before A

    # find all nodes that do not have any prereqs at all
    for node in range(0, ncourses):
        no_prereqs = True
        for edge in edges:
            if edge[1] == node:
                no_prereqs = False
                break
        if no_prereqs:
            stk.append(node)

    # Starting with the courses without prereqs, find
    # courses that rely on those, and work down.
    while len(stk) > 0:
        node = stk.pop()
        processed.add(node)

        for edge in edges:
            if edge[0] == node:
                if edge[1] not in processed:
                    stk.append(edge[1])
                else:
                    # if a node has been previously processed,
                    # there is a circular dependency
                    return False

    return len(processed) == ncourses

rc = course_schedule(2, [[1,0]])
assert(rc)

rc = course_schedule(2, [[1,0], [0, 1]])
assert(not rc)

rc = course_schedule(3, [[1,0], [2, 1]])
assert(rc)

rc = course_schedule(4, [[1,0], [2, 1], [3, 2]])
assert(rc)

rc = course_schedule(4, [[1,0], [2, 1], [3, 2], [2, 3]])
assert(not rc)

# implicit course 4
rc = course_schedule(5, [[1,0], [2, 1], [3, 2]])
assert(rc)

# loop 
rc = course_schedule(5, [[1,0], [2, 1], [3, 2], [1, 4], [4, 2]])
assert(not rc)
