# 2024-11-14: This is still wrong. Hash sets are randomized
# order, sorting them yields an edge case such as '..',
# where '..' should be any two letter word, but AFAIK,
# I'm not handling this properly
from pprint import pprint
from typing import List

class WordDictionary:

    def __init__(self):
        self.trie = []

    def addWord(self, word: str) -> None:
        print("adding " + word)
        for i in range(len(word)):
            if i >= len(self.trie):
                self.trie.append(dict())
            if word[i] not in self.trie[i]:
                self.trie[i][word[i]] = set()

            if i > 0:
                self.trie[i - 1][word[i - 1]].add(word[i])

            if i == len(word) - 1:
                self.trie[i][word[i]].add("!")

        # pprint(self.trie)


    def search(self, word: str) -> bool:
        N = len(word)

        if N > len(self.trie):
            return False

        if word[0] != '.' and word[0] not in self.trie[0]:
            return False


        stk = []

        # populate stack

        if word[0] == '.':
            for x in sorted(self.trie[0].keys()):
                if x != "!":
                    stk.append((x, 0))
        else:
            stk.append((word[0], 0))

        print(f"searching: {word} {len(stk)}")
        while len(stk) > 0:
            pprint(stk)
            elem = stk.pop()
            s = elem[0]
            i = elem[1]

            # end of string, check for terminal (in case of substring, eg bat vs bate)
            print("popped:", s, i, len(stk))
            if i == N - 1:
                print(s, i)
                pprint(self.trie[i][s])
                if "!" in self.trie[i][s]:
                    return True
                continue
            nxt = word[i + 1]

            if nxt == '.':
                # wildcard, check all values at this level
                for x in sorted(self.trie[i][s]):
                    # if x != "!":
                    #     stk.append((x, i + 1))
                    if x != "!" and x in self.trie[i][s]:
                        stk.append((x, i + 1))
            else:
                if nxt in self.trie[i][s]:
                    stk.append((nxt, i + 1))

        return False

def solve(op, data, expected):
    wd = WordDictionary()
    for i in range(1, len(op)):
        f = getattr(wd, op[i])
        res = f(*data[i])
        # print(op[i], data[i], res, expected[i])
        assert(res == expected[i])
    return wd

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)

# op = ["WordDictionary","addWord","addWord","addWord","search","search","search","search", "addWord", "search"]
# data = [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."],["fn"],[".."]]
# expected = [None,None,None,None,False,True,True,True,None,True]

# solve(op, data, expected)

code = open("data.py").read()
obj = eval(code)
# pprint(obj)

wd = solve(obj[0], obj[1], obj[2])
assert(wd.search(".."))
