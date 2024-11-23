class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = left + ((right - left) // 2)

            if nums[mid] == target:
                return mid

            pivoted = nums[left] > nums[right]

            if pivoted:
                if nums[mid] > nums[left]:
                    if nums[mid] < target:
                        right = mid - 1
                    else:
                        left = mid + 1
                else:
                    if nums[mid] > target:
                        right = mid - 1
                    else:
                        left = mid + 1
                continue

            if target > nums[mid]:
                left = mid + 1
            else:
                right = mid - 1

        return -1
