# 2024-12-12: I don't think I'd be able to recall this
# in an interview setting. The key thing here in this problem
# is that deletion works by updating a value with a
# predecessor/successor, then recursively finding that
# key and deleting it further down the tree. The node
# itself is not removed (I was imagining some kind of
# tree rotation)
class Solution:
    def successor(self, root):
        root = root.right
        while root.left:
            root = root.left
        return root.val
    def predecessor(self, root):
        root = root.left
        while root.right:
            root = root.right
        return root.val
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None

        if key > root.val:
            root.right = self.deleteNode(root.right, key)
        elif key < root.val:
            root.left = self.deleteNode(root.left, key)
        else:
            if not (root.left or root.right):
                root = None
            elif root.right:
                root.val = self.successor(root)
                root.right = self.deleteNode(root.right, root.val)
            else:
                root.val = self.predecessor(root)
                root.left = self.deleteNode(root.left, root.val)
        return root

