# 2024-11-23: Okay I spent many hours trying to come up
# with something based on the hints that it was binary
# search. One thing: my left/right dyslexia did not
# come in handy for me. Two: You can apparently do
# more than one binary search and have it still be okay.
# I only had time to code up the first approach. I did
# not look at the code for this one, and managed to
# just get something working looking at the algorithm
# instructions.
class Solution:
    # approach 1: find pivot index + binary search
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] > nums[-1]:
                left = mid + 1
            else:
                right = mid - 1

        pivot = left

        def binarysearch(nums, left, right):
            while left <= right:
                mid = left + (right - left) // 2
                if nums[mid] < target:
                    left = mid + 1
                elif nums[mid] > target:
                    right = mid - 1
                else:
                    return mid

            return -1

        # perform binary search over nums[0 ~ pivot - 1]

        idx = binarysearch(nums, 0, pivot - 1)

        if idx >= 0:
            return idx

        # perform binary search over nums[pivot ~ len(nums) - 1]

        return binarysearch(nums, pivot, len(nums) - 1)
