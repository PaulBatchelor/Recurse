# 2025-01-05 Another attempt. I managed to do it without
# looking up the answer. I glanced at my solution
# from novemember 2024, and the answer I had seems to 
# use recursion, while this version I have makes use
# of an explicit stack


class Trie:
    def __init__(self):
        self.children = {}
        self.terminal = False

class WordDictionary:
    def __init__(self):
        self.root = Trie()

    def addWord(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Trie()
            node = node.children[c]
        node.terminal = True

    def search(self, word: str) -> bool:
        stk = []
        stk.append((self.root, 0))
        while stk:
            node, pos = stk.pop()
            
            if pos > len(word):
                return False
            
            if pos == len(word):
                if node.terminal:
                    return True
                continue
            
            if word[pos] == '.':
                # wildcard, try paths from all children
                for child in node.children.values():
                    stk.append((child, pos + 1))
                continue
            
            if word[pos] not in node.children:
                continue
            
            stk.append((node.children[word[pos]], pos + 1))
        return False
        


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)

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
