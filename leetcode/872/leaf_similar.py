# 2024-12-10: I did what I thought was the "brute force"
# solution, saw how slow it was, and assumed there was
# a faster approach that I could do using a stack.
# The editorial was basically just what I did, only
# with generator iterators, which I didn't know about
class Solution:
    # same approach as what I originally, only using
    # generator iterators
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        def dfs(node):
            if node:
                if not node.left and not node.right:
                    yield node.val
                yield from dfs(node.left)
                yield from dfs(node.right)

        return list(dfs(root1)) == list(dfs(root2))
    def createLeafSequence(self, root: Optional[TreeNode]) -> List[int]:
        lseq = []
        def dfs(node):
            if not node:
                return

            # inorder traversal
            if node.left:
                dfs(node.left)

            if node.left is None and node.right is None:
                lseq.append(node.val)

            if node.right:
                dfs(node.right)

        dfs(root)
        return lseq
    def leafSimilarV1(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:

        lseq1 = self.createLeafSequence(root1)
        lseq2 = self.createLeafSequence(root2)

        pprint(lseq1)
        pprint(lseq2)
        return lseq1 == lseq2

