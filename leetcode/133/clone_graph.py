# 2024-11-19 I came up with a two-step BFS process for this.
# the editorial had something a little bit more slick, which
# I also included here.
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
from collections import deque

class Solution:
    # version 2 (based on editorial): BFS that appends neighbors as it goes
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        q = deque()
        visited = {}
        if node is None:
            return None

        q.append(node)

        visited[node.val] = Node(val=node.val, neighbors = [])
        while len(q) > 0:
            node = q.popleft()

            for neighbor in node.neighbors:
                if neighbor.val not in visited:
                    visited[neighbor.val] = Node(val=neighbor.val, neighbors=[])
                    q.append(neighbor)
                visited[node.val].neighbors.append(visited[neighbor.val])

        return visited[1]

    # my first attempt without help: a two-step BFS process, first finding
    # the nodes, then updating the links to the nodes
    def cloneGraphV1(self, node: Optional['Node']) -> Optional['Node']:
        nodelist = {}

        if node is None:
            return None

        # first, allocate all the nodes using BFS, using the
        # old neighbors

        q = deque()

        q.append(node)

        while len(q) > 0:
            node = q.popleft()
            if node.val in nodelist:
                continue

            nodelist[node.val] = Node(val=node.val, neighbors=node.neighbors)

            for n in node.neighbors:
                q.append(n)

        # then, once all the nodes have been created,
        # update all the neighbors for every node

        for _,node in nodelist.items():
            copied_neighbors = []
            for nd in node.neighbors:
                copied_neighbors.append(nodelist[nd.val])
            node.neighbors = copied_neighbors

        # return the top node (node with value 1)
        return nodelist[1]
