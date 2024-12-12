# 2024-12-12: Implemetned after reading editorial, and
# doing problem 560. I think I had the same hang-ups as
# last time.
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        h = defaultdict(int)
        count = 0
        def dfs(node, cursum):
            nonlocal count, h
            if node is None:
                return
            cursum += node.val
            if cursum == targetSum:
                count += 1
            count += h[cursum - targetSum]
            h[cursum] += 1
            dfs(node.left, cursum)
            dfs(node.right, cursum)
            h[cursum] -= 1

        dfs(root, 0)

        return count
