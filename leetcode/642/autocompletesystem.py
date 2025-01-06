# 2025-01-05: Did this one while working through the
# Trie explore card.

class Trie:
    def __init__(self):
        self.children = {}
        self.parent = None
        self.count = 0

    def insert(self, sentence, count):
        node = self
        for c in sentence:
            if c not in node.children:
                node.children[c] = Trie()
                node.children[c].parent = node
            node = node.children[c]
        # update, don't overwrite.
        node.count += count


class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = Trie()
        self.last = self.root
        self.curstr = ""
        n = len(sentences)
        for i in range(n):
            #print(sentences[i])
            self.root.insert(sentences[i], times[i])

    def input(self, c: str) -> List[str]:
        last = self.last
        if c == '#':
            self.root.insert(self.curstr, 1)
            # reset cache
            self.last = self.root
            self.curstr = ""
            return []

        self.curstr += c
    
        if not last:
            return []
        # no matching sentences with prefix
        if c not in last.children:
            self.last = None
            return []

        last = last.children[c]

        self.last = last

        h = []

        stk = []

        stk.append((last, ""))

        # traverse through nodes in subtree
        while stk:
            node, path = stk.pop()
            if node.count > 0:
                heapq.heappush(h, (-node.count, self.curstr + path))
                #heapq.heappop(h)
            
            for ch in node.children:
                nd = node.children[ch]
                stk.append((nd, path + ch))
        hot = []

        for _ in range(min(3, len(h))):
            _,s = heapq.heappop(h)
            hot.append(s)

        return hot


# Your AutocompleteSystem object will be instantiated and called as such:
# obj = AutocompleteSystem(sentences, times)
# param_1 = obj.input(c)
