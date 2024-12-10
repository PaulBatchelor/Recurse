# 2024-12-10: somehow managed to grok the recursive structure
# on this one quite quickly, having struggled on this one
# previously

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        count = 0
        def dfs(node, max_so_far):
            if not node:
                return
            nonlocal count
            if node.val >= max_so_far:
                max_so_far = node.val
                count += 1
            dfs(node.left, max_so_far)
            dfs(node.right, max_so_far)

        dfs(root, root.val)
        return count
