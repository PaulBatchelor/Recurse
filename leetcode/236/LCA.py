# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def __init__(self):
        self.stack = []
        self.lca_node = None

    def dfs(self, node, target):
        if node is None:
            return False
        if node.val == target.val:
            return True
        return self.dfs(node.left, target) or self.dfs(node.right, target)
        
    def lca_dfs(self, root, p, q):
        if root is None:
            return False

        print(root.val)
        mid = root.val in (p.val, q.val)

        if mid:
            print(f"found: {root.val}")
            left = self.lca_dfs(root.left, p, q)
            right = self.lca_dfs(root.right, p, q)
            total = sum((mid, left, right))
            if total >= 2:
                self.lca_node = root
            return True
        
        left = self.lca_dfs(root.left, p, q)
        right = self.lca_dfs(root.right, p, q)
    
        if sum((left, right)) == 2:
            self.lca_node = root

        return left or right
    
    # recursive DFS after reading editorial
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        self.lca_node = root
        self.lca_dfs(root, p, q)
        return self.lca_node

    # OLD VERSION with stack trace
    def lowestCommonAncestor2(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None:
            return None
        
        print(root.val)
        self.stack.append(root)
        if root.val in (p.val, q.val):
            other = p
            print(f"found {root.val}")
            if root.val == p.val:
                other = q
            stack = self.stack
            while len(stack) > 0:
                n = stack.pop()
                if self.dfs(n, other):
                    return n
        #self.stack.append(root)
        return self.lowestCommonAncestor(root.left, p, q) or self.lowestCommonAncestor(root.right, p, q)
    def lowestCommonAncestor3(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None:
            return None

        if root.val in (p.val, q.val):
            return root
        # print(root.val, p.val, q.val)

        if root.left and root.left.val in (p.val, q.val):
            # LCA is either root or left
            selected = p
            if root.left.val == selected.val:
                selected = q
            # print(f"found: {selected}")
            # setting p == q is a bit of a hack that allows for a DFS single-value search
            a = self.lowestCommonAncestor(root.left, selected, selected)
            if a is None:
                return root
            return root.left
        
        # do similar check for righthand side
        if root.right and root.right.val in (p.val, q.val):
            # LCA is either root or left
            selected = p
            if root.right.val == selected.val:
                selected = q
            # setting p == q is a bit of a hack that allows for a DFS single-value search
            a = self.lowestCommonAncestor(root.right, selected, selected)
            if a is None:
                return root
            return root.right
        
        # neither p or q found, traverse left/right
        return self.lowestCommonAncestor(root.left, p, q) or self.lowestCommonAncestor(root.right, p, q)
            
    def lowestCommonAncestor2(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # check and see if children are p and q
        left = root.left
        right = root.right

        if left and (left.val == q or left.val == p):
            searchfor = q                
            if left.val == q:
                searchfor = p
            if self.dfs(left, searchfor):
                return left.val
            else:
                return root.val
        
        if right:
            if right.val == p:
                pass
            elif right.val == q:
                pass

        # find the corresponding node using DFS
        # if the other node is in the opposite child,
        # then the LCA is the current parent, otherwise
        # it is the corresponding child node
        
        return None
