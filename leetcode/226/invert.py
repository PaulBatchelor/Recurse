from pprint import pprint

class BinaryTree:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
    def print(self):
        if self.left is not None:
            self.left.print()
        if self.val is not None:
            print(self.val)
        if self.right is not None:
            self.right.print()
    def inorder(self, lst):
        if self.left is not None:
            self.left.inorder(lst)
        if self.val is not None:
            lst.append(self.val)
        if self.right is not None:
            self.right.inorder(lst)

def invert(root):
    if root is None:
        return root

    left = root.left
    right = root.right

    root.left = invert(right)
    root.right = invert(left)


    return root

def tree1():
    T = BinaryTree(4)

    T.left = BinaryTree(2)
    T.right = BinaryTree(7)

    T.left.left = BinaryTree(1)
    T.left.right = BinaryTree(3)

    T.right.left = BinaryTree(6)
    T.right.right = BinaryTree(9)

    return T

def tree2():
    T = BinaryTree(2)
    T.left = BinaryTree(1)
    T.right = BinaryTree(3)

    return T

T = tree1()
T = invert(T)

lst = []

T.inorder(lst)

assert(lst == [9, 7, 6, 4, 3, 2, 1])

T = tree2()
T = invert(T)

lst = []

T.inorder(lst)

assert(lst == [3, 2, 1])
