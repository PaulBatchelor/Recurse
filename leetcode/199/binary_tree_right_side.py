@2024-10-24: solution recalled from a few months ago
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        inner = []
        outer = []
        results = []
        if root is None: return []
        outer.append(root)
        while len(outer) > 0:
            results.append(outer[-1].val)
            for node in outer:
                if node is None:
                    continue
                if node.left is not None:
                    inner.append(node.left)
                if node.right is not None:
                    inner.append(node.right)
            outer = inner
            inner = []

        return results

# BFS: use queue to load up each "layer", and somehow retrieve the rightmost end of it
# double queues I think is how this one is typically solved

# add 1 to outer queue, and append to output
# iterate over outer queue [1]
# inner queue: 2, 3
# add last item of inner queue to output
# inner queue becomes outer queue, start new inner queue
# iterate over outer queue: 2, 3
# inner queue: 5, 4
# add last item of inner queue to output
# inner queue becomes outer queue, start new inner queue
# queue is zero, break out of loop
# return output
