# 2025-01-05: Done as part of the Trie explore card

class Trie:
    def __init__(self):
        self.children = {}
        self.terminal = False
    def insert(self, word):
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = Trie()
            node = node.children[c]
        node.terminal = True
    def prefix(self, word):
        node = self
        size = 0

        for c in word:
            if node.terminal:
                return word[:size]
            if c not in node.children:
                return word
            size += 1
            node = node.children[c]
        return word
    

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        words = sentence.split()
        t = Trie()

        for w in dictionary:
            t.insert(w)

        for i in range(len(words)):
            words[i] = t.prefix(words[i])

        return " ".join(words)
