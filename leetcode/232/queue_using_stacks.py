# 2024-11-25: wow. this problem. the solution I came up
# had me shaking my head going no it can't be. but they
# accepted it.

# Version 2: Stack 2 is only used in the push operation
# as an intermediate holding ground to push an element,
# making in an O(n) operation. The others are O(1)

class MyQueue:

    def __init__(self):
        self.front = None
        self.s1 = []
        self.s2 = []


    def push(self, x: int) -> None:
        if not self.s1:
            self.front = x

        while self.s1:
            self.s2.append(self.s1.pop())

        self.s2.append(x)
        while self.s2:
            self.s1.append(self.s2.pop())

    def pop(self) -> int:
        res = self.s1.pop()
        if self.s1:
            self.front = res
        return res

    def peek(self) -> int:
        return self.front

    def empty(self) -> bool:
        return len(self.s1) == 0



# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()

# Version 1: LOL. this feels very bruteforce. Every operation,
# turn a stack into a queue by moving everything over
class MyQueue_bruteforce:

    def __init__(self):
        self.stk1 = []
        self.stk2 = []

    def repopulate(self, a, b):
        while a:
            b.append(a.pop())

    def push(self, x: int) -> None:
        self.stk1.append(x)

    def pop(self) -> int:
        self.repopulate(self.stk1, self.stk2)
        elem = self.stk2.pop()
        self.repopulate(self.stk2, self.stk1)
        return elem
    def peek(self) -> int:
        self.repopulate(self.stk1, self.stk2)
        elem = self.stk2[-1]
        self.repopulate(self.stk2, self.stk1)
        return elem

    def empty(self) -> bool:
        return len(self.stk1) == 0
