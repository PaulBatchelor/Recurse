# mostly untested, but I bet it's at least 90% correct.
# this is graph traversal problem (BFS or DFS could work,
# but BFS makes more sense). Some bookkeeping required
# to manage previous allocated and visited nodes.

from copy import deepcopy
from collections import deque
from pprint import pprint

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node):
    # use queue for BFS
    q = deque()

    # hashmap to keep track of allocated nodes
    # lookup table h[id] -> node
    h = dict()

    # a set to keep track of which nodes have been traversed
    # each node should be visited exactly once
    visited = set()

    # add the first node to the queue, and make an initial
    # copy. neighbors will be added later
    q.append(node)
    visited.add(node.val)
    h[node.val] = Node(node.val)

    while len(q) > 0:
        node = q.popleft()

        # the new node is always going to be allocated
        # when the old node is added to the queue
        newnode = h[node.val]
        path = []

        # iterate over the neighbors and traverse
        for n in node.neighbors:
            # a neighbor will be seen as a neighbor
            # before it is visited, and may be a neighbor
            # to more than one node. keep track which
            # nodes have been allocated in the hashmap
            if n.val not in h:
                h[n.val] = Node(n.val)

            # update the neighbors field with the new
            # node reference
            newnode.neighbors.append(h[n.val])

            # add to queue if neighborly node hasn't been
            # visisted yet
            if n.val not in visited:
                q.append(n)
                visited.add(n.val)

    return h[1]

def graph1():
    nodes = [Node(i + 1) for i in range(4)]

    nodes[0].neighbors = [nodes[1], nodes[3]]
    nodes[1].neighbors = [nodes[0], nodes[2]]
    nodes[2].neighbors = [nodes[1], nodes[3]]
    nodes[3].neighbors = [nodes[0], nodes[2]]

    return nodes[0]

# generate adjacency list, made using a hashmap instead of
# an array.
def adjlist(gr):
    visited = set()
    adj = {}
    q = deque()

    q.append(gr)

    while len(q) > 0:
        node = q.popleft()
        adj[node.val] = []
        for n in node.neighbors:
            adj[node.val].append(n.val)
            if n.val not in visited:
                q.append(n)
                visited.add(n.val)

    return adj

graph = graph1()
graph2 = clone_graph(graph)

a1 = adjlist(graph)
a2 = adjlist(graph2)

assert(a1 == a2)
