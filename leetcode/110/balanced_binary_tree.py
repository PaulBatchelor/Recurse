# 2024-11-25: I hacked together the correct recursive
# solution, after some initial attempts and quick fixes.
# I've adapted a version of the top-down recursive editorial solution
# as well, as it seems to be a bit cleaner.

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    # based off top-down recursive answer from editorial, which is
    # similar to what I came up with
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        def height(root):
            if not root:
                return 0
            return 1 + max(height(root.left), height(root.right))

        return (
            abs(height(root.left) - height(root.right)) < 2
            and self.isBalanced(root.left)
            and self.isBalanced(root.right)
        )
    # recursive solution I came up with
    def isBalancedV1(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        self.balanced = True
        def getHeight(node, height=0):
            if not node:
                return height

            lh = getHeight(node.left, height + 1)
            rh = getHeight(node.right, height + 1)

            if self.balanced and abs(lh - rh) > 1:
                self.balanced = False

            return max(lh,rh)

        getHeight(root, 0)
        return self.balanced

