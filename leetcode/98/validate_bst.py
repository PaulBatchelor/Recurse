# 2024-11-22: Ultimately gave up after 50 minutes of
# trying to figure out. I had an initial idea that failed
# because I wasn't handling ranges correctly, but I was
# starting to build an intuition. The in-order traversal
# approach for validating the BST was pretty clever, I
# can imagine myself going with that solution in a real
# interview setting.

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def inorder(root):
            if not root:
                return True
            if not inorder(root.left):
                return False
            if root.val <= self.prev:
                return False
            self.prev = root.val
            return inorder(root.right)

        self.prev = -math.inf
        return inorder(root)

    # iterative traversal with valid range:
    def isValidBST_iterative_validrange(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        stack = []

        stack.append((root, -math.inf, math.inf))

        while stack:
            node, lower, upper = stack.pop()
            if not node:
                continue

            val = node.val
            if val <= lower or val >= upper:
                return False
            stack.append((node.left, lower, val))
            stack.append((node.right, val, upper))

        return True
    # recursive traversal with valid range
    def isValidBST_rev_validrange(self, root: Optional[TreeNode]) -> bool:
        def validate(node, low=-math.inf, high=math.inf):
            if not node:
                return True
            if node.val <= low or node.val >= high:
                return False

            return validate(node.right, node.val, high) and validate(node.left, low, node.val)

        return validate(root)


    def isValidBST1(self, root: Optional[TreeNode]) -> bool:
        # reached a leaf
        if root is None:
            return True

        if root.left is not None:
            if root.left.val >= root.val:
                return False

            if root.left.right is not None and root.left.right.val >= root.val:
                return False

            # TODO: merge conditionals?
            if not self.isValidBST(root.left):
                return False

        if root.right is not None:
            if root.right.val <= root.val:
                return False

            if root.right.left is not None and root.right.left.val <= root.val:
                return False

            if not self.isValidBST(root.right):
                return False

        return True


