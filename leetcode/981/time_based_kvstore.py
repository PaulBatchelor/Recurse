# My first naive attempt was too slow, then I optimized
# get to be divide an conquer instead of a linear sweep

class TimeMap:
    def __init__(self):
        self.lookup = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.lookup:
            self.lookup[key] = []
        self.lookup[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.lookup:
            return ""
        entry = self.lookup[key]

        left = 0
        right = len(entry) - 1

        found = -1

        while (left <= right):
            mid = left + (right - left)//2

            if entry[mid][0] > timestamp:
                right = mid - 1
            else:
                if found < 0:
                    found = mid
                if entry[mid][0] >= entry[found][0]:
                    found = mid
                left = mid + 1
        
        if found < 0:
            return ""
        return entry[found][1]
        
# love high 10
# love low 20

# foo bar 1
# foo bar2 4

# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
