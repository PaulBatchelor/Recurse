class BinaryTree:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def tree1():
    root = BinaryTree(2)
    root.left = BinaryTree(1)
    root.right = BinaryTree(3)
    return root

def tree2():
    root = BinaryTree(5)
    root.left = BinaryTree(1)
    root.right = BinaryTree(4)
    root.right.left = BinaryTree(3)
    root.right.right = BinaryTree(6)
    return root

def isValidTree(root):
    if root is None:
        return True

    if root.left is not None and root.left.val > root.val:
        return False

    if root.right is not None and root.right.val < root.val:
        return False

    return isValidTree(root.left) and isValidTree(root.right)

tree = tree1()
rc = isValidTree(tree)
assert(rc)

tree = tree2()
rc = isValidTree(tree)
assert(not rc)
