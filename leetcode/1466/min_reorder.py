# 2024-12-13 Got most of this logic correct. My frist
# trip-up was forgetting to exclude city 0 from traversal
# My second trip-up was forgetting about adding a
# "phantom edge" and encoding direction. Both were fixed
# within the 45 minute timeframe.

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        adj = defaultdict(list)
        visited = set()
        stk = []
        nchanges = 0
        for edge in connections:
            adj[edge[0]].append((edge[1], 1))
            adj[edge[1]].append((edge[0], 0))
            # add nodes leading into zero pre-emptively for traversal
            if edge[1] == 0 and edge[0] not in visited:
                visited.add(edge[0])
                stk.append(edge[0])

        stk.append(0)
        visited.add(0)

        while stk:
            curcity = stk.pop()
            for city, direction in adj[curcity]:
                if city not in visited:
                    visited.add(city)
                    stk.append(city)
                    nchanges += direction

        return nchanges

