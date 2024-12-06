# 2024-12-06: most of this was stumbling around the python docs
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        nums1 = set(nums1)
        nums2 = set(nums2)
        common = nums1 & nums2 #nums1.intersection(nums2)

        return [list(nums1 - common), list(nums2 - common)]
