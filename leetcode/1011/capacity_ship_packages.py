from typing import List
class Solution:
    def possible(self, capacity, weights, days):
        acc = 0
        days_left = days - 1
        items_left = len(weights)

        for w in weights:
            if days_left == items_left:
                return True
            acc += w
            # print(f"weight {w}")
            if acc > capacity:
                acc = w
                days_left -= 1
                # print(f"days left: {days_left}")

            items_left -= 1

        return days_left == 0

    def shipWithinDays(self, weights: List[int], days: int):
        left = max(weights)
        right = sum(weights)

        while (left <= right):
            # print(left, right)
            if left == right:
                return left
            mid = left + (right - left)//2 
            is_possible = self.possible(mid, weights, days)
            # print(f"possible {mid}: {is_possible}")
            if is_possible:
                right = mid
            else:
                left = mid + 1

        return -1

s = Solution()

ret = s.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
assert(ret == 15)

ret = s.shipWithinDays([3, 2, 2, 4, 1, 4], 3)
assert(ret == 6)

ret = s.shipWithinDays([1, 2, 3, 1, 1], 4)
assert(ret == 3)
