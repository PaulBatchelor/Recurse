# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree_r(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if len(preorder) == 0:
            return None

        root = preorder.pop()
        left = None

        # Traverse left if root isn't leftmost value in inorder stack

        # if root is not current inorder value, return None
        # left should be none I think if the preorder/inorder lists are valid
        if inorder[-1] != root:
            left = self.buildTree_r(preorder, inorder)

        # this logic needed in order for backtracking logic to work
        if inorder[-1] != root:
            # push back onto stack
            preorder.append(root)
            return None

        # pop inorder value (root val), and traverse right
        inorder.pop()

        right = self.buildTree_r(preorder, inorder)
        # create new node with root, left, right, values
        return TreeNode(val=root, left=left, right=right)

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        preorder.reverse()
        inorder.reverse()
        return self.buildTree_r(preorder, inorder)
