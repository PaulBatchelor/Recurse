# 2024-11-26: Once again, I quickly banged out a recursive
# solution, only to find that a better version of my
# approach existed. I also added the tail recursion BFS
# approach.

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    # BFS + tail recursion
    def maxDepth_rec(self):
        if not self.next_items:
            return self.max_depth
        next_node, next_level = self.next_items.pop()
        next_level += 1
        self.max_depth = max(self.max_depth, next_level)

        if next_node.left:
            self.next_items.append((next_node.left, next_level))
        if next_node.right:
            self.next_items.append((next_node.right, next_level))

        return self.maxDepth_rec()
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        self.next_items = []
        self.max_depth = 0
        self.next_items.append((root, 0))
        return self.maxDepth_rec()
    # looks like my recursive solution could have been simplified
    def maxDepthV2(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        lh = self.maxDepth(root.left)
        rh = self.maxDepth(root.right)
        return max(lh, rh) + 1
    # my original solution
    def maxDepthV1(self, root: Optional[TreeNode]) -> int:
        def getHeight(node):
            if not node:
                return 0

            lh = getHeight(node.left)
            rh = getHeight(node.right)

            return 1 + max(lh, rh)

        return getHeight(root)
