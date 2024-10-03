# verified as working in LC editor
# I looked up the answer because I had no idea how I'd
# be able to do this in O(1) time. This is one of those
# prolems where you either know the "trick" or you don't.
# And if you know the trick, the code is trivial.

class MinStack:
    def __init__(self):
        self.min_val = None
        self.min_idx = -1
        self.stack = []
        self.pos = -1
        self.mins = []
        

    def push(self, val: int) -> None:
        self.pos += 1
        if self.min_val is None or val <= self.min_val:
            self.min_val = val
            self.min_idx = self.pos
        self.stack.append(val)
        self.mins.append(self.min_idx)

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()
        self.pos -= 1
        

    def top(self) -> int:
        return self.stack[self.pos]
        

    def getMin(self) -> int:
        return self.stack[self.mins[self.pos]]

