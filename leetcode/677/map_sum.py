# 2025-01-05: Done during Trie explore card

class MapSum:
    def __init__(self):
        self.children = {}
        self.value = None

    def insert(self, key: str, val: int) -> None:
        node = self
        for c in key:
            if c not in node.children:
                node.children[c] = MapSum()
            node = node.children[c]
        node.value = val

    def sum(self, prefix: str) -> int:
        node = self
        for c in prefix:
            if c not in node.children:
                return 0
            node = node.children[c]
        
        total = 0

        stk = []
        stk.append(node)
        while stk:
            node = stk.pop()
            if node.value:
                total += node.value
            for n in node.children.values():
                stk.append(n)

        return total

