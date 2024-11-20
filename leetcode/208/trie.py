# 2024-11-20: I've done enough trie problems at this point
# that the code is muscle memory

class Trie:
    def __init__(self):
        self.word = False
        self.children = {}

    def insert(self, word: str) -> None:
        node = self
        for w in word:
            if w not in node.children:
                node.children[w] = Trie()
            node = node.children[w]
        node.word = True


    def search(self, word: str) -> bool:
        node = self
        for w in word:
            if w not in node.children:
                return False
            node = node.children[w]
        return node.word

    def startsWith(self, prefix: str) -> bool:
        node = self
        for p in prefix:
            if p not in node.children:
                return False
            node = node.children[p]
        return True



# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
