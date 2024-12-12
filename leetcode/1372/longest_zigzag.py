# 2024-12-12: I did it, and I looked up some solutions
# this seems to be pretty much the way to do it

class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        maxcount = 0

        def dfs(node, direction, curcount):
            if not node:
                return
            nonlocal maxcount
            maxcount = max(maxcount, curcount)

            # left -> right
            if direction == 0:
                dfs(node.left, 0, 1)
                dfs(node.right, 1, curcount + 1)
            # right -> left
            else:
                dfs(node.left, 0, curcount + 1)
                dfs(node.right, 1, 1)

        dfs(root.left, 0, 1)
        dfs(root.right, 1, 1)

        return maxcount
