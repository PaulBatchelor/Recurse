# 2024-11-24: I didn't grok it, so I had to look it up

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    # iterative, adapted from recursive approach
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        p_val = p.val
        q_val = q.val

        while root:
            # right subtree
            if p_val > root.val and q_val > root.val:
                root = root.right
                continue
            # left subtree
            if p_val < root.val and q_val < root.val:
                root = root.left
                continue
            break

        return root

    # recursive approach
    def lowestCommonAncestor_rec(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        parent_val = root.val

        p_val = p.val
        q_val = q.val

        # both p and q nodes in the right subtree
        if p_val > parent_val and q_val > parent_val:
            return self.lowestCommonAncestor(root.right, p, q)

        # both p and q nodes in the left subtree
        if p_val < parent_val and q_val < parent_val:
            return self.lowestCommonAncestor(root.left, p, q)

        return root

