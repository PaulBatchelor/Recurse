# 2024-11-21: Again, not a very satisfying problem. I
# remember needing to look up the answer and being kind
# of disappointed by it

# The clever-er solution using a "min-tracker" stack
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_tracker = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if len(self.min_tracker) == 0 or val <= self.min_tracker[-1]:
            self.min_tracker.append(val)

    def pop(self) -> None:
        v = self.stack.pop()
        if v == self.min_tracker[-1]:
            self.min_tracker.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_tracker[-1]

class MinStack1:

    def __init__(self):
        self.stk = []
        self.min_stk = []

    def push(self, val: int) -> None:
        self.stk.append(val)
        min_val = val if len(self.min_stk) == 0 else min(self.min_stk[-1], val)
        self.min_stk.append(min_val)

    def pop(self) -> None:
        self.stk.pop()
        self.min_stk.pop()


    def top(self) -> int:
        return self.stk[-1]


    def getMin(self) -> int:
        return self.min_stk[-1]



# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()


# This uses two stacks, which is similar the tuple-stack
# used in one of the solutions in the editorial
class MinStackV1:

    def __init__(self):
        self.stk = []
        self.min_stk = []

    def push(self, val: int) -> None:
        self.stk.append(val)
        min_val = val if len(self.min_stk) == 0 else min(self.min_stk[-1], val)
        self.min_stk.append(min_val)

    def pop(self) -> None:
        self.stk.pop()
        self.min_stk.pop()


    def top(self) -> int:
        return self.stk[-1]


    def getMin(self) -> int:
        return self.min_stk[-1]



# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
