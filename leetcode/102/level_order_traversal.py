from collections import deque
from pprint import pprint

class Node:
    def __init__(self, val, left=None, right=None):
        self.left = left
        self.right = right
        self.val = val

def level_order_trav(root):
    res = []

    if root == None:
        return []

    q = deque()

    q.append(root)
    res.append([root.val])

    while len(q) > 0:
        node = q.popleft()
        pair = []
        if node.left is not None:
            q.append(node.left)
            pair.append(node.left.val)
        if node.right is not None:
            q.append(node.right)
            pair.append(node.right.val)

        if len(pair) > 0:
            res.append(pair)

    return res

def tree1():
    root = Node(3)
    root.left = Node(9)
    root.right = Node(20)
    root.right.left = Node(15)
    root.right.right = Node(7)

    return root

def tree2():
    root = Node(1)
    return root

def tree3():
    root = Node(3)
    root.left = Node(9)
    root.left.right = Node(8)
    root.right = Node(20)
    root.right.left = Node(15)
    root.right.right = Node(7)

    return root

tree = tree1()
res = level_order_trav(tree)
assert(res == [[3], [9, 20], [15, 7]])

tree = tree2()
res = level_order_trav(tree)
assert(res == [[1]])

tree = tree3()
res = level_order_trav(tree)
assert(res == [[3], [9, 20], [8], [15, 7]])
