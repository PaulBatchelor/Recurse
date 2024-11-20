from pprint import pprint

class Trie:
    def __init__(self, val=None):
        self.children = {}
        self.val = val
        self.end = False

    def insert(self, word: str) -> None:
        node = self
        for s in word:
            if s not in node.children:
                node.children[s] = Trie(s)
            node = node.children[s]
        node.end = True

    def search(self, word: str) -> bool:
        node = self
        for s in word:
            if s not in node.children:
                return False
            node = node.children[s]

        return node.end

    def startsWith(self, prefix: str) -> bool:
        node = self
        for s in prefix:
            if s not in node.children:
                return False
            node = node.children[s]

        return True

def test():
    cmds = ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
    inputs = [[], "apple", "apple", "app", "app", "app", "app"]
    expected = [None, None, True, False, True, None, True]
    obj = None

    outputs = []

    for i in range(0, len(cmds)):
        result = None
        match cmds[i]:
            case "Trie":
                obj = Trie()
            case "insert":
                obj.insert(inputs[i])
            case "search":
                result = obj.search(inputs[i])
            case "startsWith":
                result = obj.startsWith(inputs[i])

        outputs.append(result)

    assert(outputs == expected)

test()
