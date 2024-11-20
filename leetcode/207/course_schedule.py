# 2024-11-20: I've done this problem, and new about Kahn's
# algorithm for cycle detection. For some reason, I have
# trouble getting the adjacency list working correctly.
# the input pairs feel backward. I managed to get it working
# thinking about it as a problem to remove leaves.
# In the editorial, I took their solution and renamed
# the generic graph variables to ones appropriate to
# the domain so I could keep track of what I was doing

from collections import deque
class Solution:
    # Editorial: Kahn's algorithm: use of indegree to keep track of incoming edges
    # reworked the variables in the code to have more domain-specfic language
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        nrequirements = [0] * numCourses
        needed_for = [[] for _ in range(numCourses)]

        for pre in prerequisites:
            needed_for[pre[1]].append(pre[0])
            nrequirements[pre[0]] += 1

        queue = deque()
        for i in range(numCourses):
            if nrequirements[i] == 0:
                queue.append(i)
        coursesTaken = 0

        while queue:
            curCourse = queue.popleft()
            coursesTaken += 1
            for course in needed_for[curCourse]:
                nrequirements[course] -= 1
                if nrequirements[course] == 0:
                    queue.append(course)

        return coursesTaken == numCourses
    # Initial approach: find leaves, and remove leaves
    def canFinishV1(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # design a structure where it's easy to find leaves
        # find initial leaves
        # remove leaves from graph
        # get new leaves
        # repeat until there are no more leaves
        # if the number of nodes visited is the number of courses, it's acylic and
        # possible to complete the courses

        adj = [set() for _ in range(numCourses)]
        courses_left = numCourses

        for p in prerequisites:
            adj[p[0]].add(p[1])

        # find initial leaves

        leaves = []

        for course, pre in enumerate(adj):
            if len(pre) == 0:
                leaves.append(course)

        while len(leaves) > 0:
            courses_left -= len(leaves)
            new_leaves = []
            for leaf in leaves:
                for course, pre in enumerate(adj):
                    if leaf in pre:
                        pre.remove(leaf)
                        if len(pre) == 0:
                            new_leaves.append(course)
            leaves = new_leaves

        return courses_left == 0
