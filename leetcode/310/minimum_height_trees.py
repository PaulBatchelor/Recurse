# 2024-11-06 Just the clever answer (that I didn't come up with)
# I went with the intuitive but too slow BFS version

from typing import List
from pprint import pprint

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return [i for i in range(n)]
        
        graph = [set() for _ in range(n)]

        for a, b in edges:
            graph[a].add(b)
            graph[b].add(a)
            print(f"{a}->{b}, {b}->{a}")

        leaves = []

        for i, nei in enumerate(graph):
            if len(nei) == 1:
                leaves.append(i)

        pprint(graph)
        
        remaining_nodes = n

        pprint(leaves)
        while remaining_nodes > 2:
            remaining_nodes -= len(leaves)
            new_leaves = []

            while leaves:
                leaf = leaves.pop()
                print(f"leaf: {leaf}")

                nei = graph[leaf].pop()
                print(f"nei: {nei}")

                graph[nei].remove(leaf)

                if len(graph[nei]) == 1:
                    new_leaves.append(nei)
                
            leaves = new_leaves
        
        return leaves

s = Solution()

n = 4
edges = [[1,0],[1,2],[1,3]]
expected = [1]
out = s.findMinHeightTrees(n, edges)
assert(out == expected)
