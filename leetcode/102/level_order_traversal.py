# 2024-11-19: Pretty run of the mill BFS stuff. The output
# was misleading in the examples. It looked like they wanted
# pairs for each node (my original untested solution did this),
# but really they wanted one for each level.

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        out = []

        q = deque()

        if root is None:
            return []

        q.append(root)

        while len(q) > 0:
            new_q = deque()
            level = []
            while len(q) > 0:
                node = q.popleft()
                level.append(node.val)
                # check left/right, append to new queue and append to level
                if node.left:
                    #level.append(node.left.val)
                    new_q.append(node.left)

                if node.right:
                    #level.append(node.right.val)
                    new_q.append(node.right)

            # append level to the output
            out.append(level)

            # update new queue to be outer queue
            q = new_q

        return out
