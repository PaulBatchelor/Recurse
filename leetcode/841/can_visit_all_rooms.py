# 2024-12-13 Pretty straight ahead
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        if not rooms:
            return True
        stk = []
        visited = set()

        stk.append(0)
        visited.add(0)

        while stk:
            room = stk.pop()

            # look at keys for unvisited rooms

            for key in rooms[room]:
                if key not in visited:
                    visited.add(key)
                    stk.append(key)

        return len(visited) == len(rooms)
