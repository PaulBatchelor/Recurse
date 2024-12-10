class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def print_nodes(n):
    if n== None:
        return

    print_nodes(n.left)
    print(n.val)
    print_nodes(n.right)

def tree1():
    root = Node(3)

    root.left = Node(1)
    root.right = Node(4)

    root.left.left = Node(3)
    root.right.left = Node(1)
    root.right.right = Node(5)

    return root

def tree2():
    root = Node(3)
    root.left = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(2)
    return root

def goodnodes(node, maxval, count):
    if node == None:
        return count

    if node.val >= maxval:
        maxval = node.val
        count += 1

    count = goodnodes(node.left, maxval, count)
    count = goodnodes(node.right, maxval, count)

    return count

root = tree1()
out = goodnodes(root, -1, 0)
assert(out == 4)

root = tree2()
out = goodnodes(root, -1, 0)
assert(out == 3)
