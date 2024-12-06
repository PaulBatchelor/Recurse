# 2024-12-06 Poured a few hours into a solution using
# a deque, then looked at the editorial

from collections import deque
class Solution:
    # editorial
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        for right in range(len(nums)):
            k -= 1 - nums[right]

            if k < 0:
                k += 1 - nums[left]
                left += 1

        return right - left + 1

    # what I hacked together
    def longestOnesV1(self, nums: List[int], k: int) -> int:
        q = deque()
        start = 0
        end = 0

        for i in range(len(nums)):
            if len(q) == k:
                break
            if nums[i] == 0:
                q.append(i)
            end = i + 1

        maxones = (end - start)

        off = end

        for i in range(off, len(nums)):
            if k == 0 and nums[i] == 0:
                start = end = -1
                continue
            if nums[i] == 1:
                if start < 0:
                    start = i
            if nums[i] == 0:
                start = q.popleft() + 1
                q.append(i)
            end = i + 1
            maxones = max((end - start), maxones)

        return maxones
