# 2024-12-08 The thing that tripped me up was which direction
# of the queue to peak at. Earlier items are to the left,
# with the leftmost being x[0], not x[-1].
from collections import deque
class RecentCounter:

    def __init__(self):
        self.queue = deque()


    def ping(self, t: int) -> int:
        # place t onto the queue
        self.queue.append(t)
        # popleft until t - end <= 3000 or queue is 1
        while self.queue and (t - self.queue[0]) > 3000:
            self.queue.popleft()
        # return length of queue
        return len(self.queue)


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)
