# 2024-11-14: This is still wrong. Hash sets are randomized
# order, sorting them yields an edge case such as '..',
# where '..' should be any two letter word, but AFAIK,
# I'm not handling this properly

# 2024-11-15: Looked up the answer. What
# you see is below. I was trying to be
# clever with my Trie, and it shot me in the foot. Tries
# need to explicitely be tries because they need to contain
# unique paths] (bad, dad, mad) don't have any prefixes
# in common, so they are each their own paths.

class Trie:
    def __init__(self):
        self.children = {}
        self.word = False

class WordDictionary:
    def __init__(self):
        self.root = Trie()

    def addWord(self, word: str) -> None:
        node = self.root
        for w in word:
            if w not in node.children:
                node.children[w] = Trie()
            node = node.children[w]
        node.word = True
    def wordSearch(self, word: str, node: Trie) -> bool:
        for i in range(len(word)):
            ch = word[i]
            if ch not in node.children:
                if ch == '.':
                    for k in node.children.keys():
                        child = node.children[k]
                        if self.wordSearch(word[i + 1:], child):
                            return True
                return False
            else:
                node = node.children[ch]
        return node.word

    def search(self, word: str) -> bool:
        # print(f"Searching {word}")
        return self.wordSearch(word, self.root)
