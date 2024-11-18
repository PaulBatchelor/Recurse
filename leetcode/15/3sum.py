# 2024-11-18: I only knew how to do the brute-force version,
# which triggered a TLE. This is from the editorial.

class Solution:
    def twoSum(self, nums: List[int], i: int, res: List[List[int]]):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            triple = nums[i], nums[lo], nums[hi]
            sm = sum(triple)
            if sm < 0:
                lo += 1
            elif sm > 0:
                hi -= 1
            else:
                res.append(triple)
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums = sorted(nums)
        res = []
        for i in range(len(nums)):
            # since the array is sorted, and the numbers
            # are checked after the index position,
            # there are no combinations that work after the numbers
            # become positive
            if nums[i] > 0:
                break
            if i == 0 or nums[i - 1] != nums[i]:
                self.twoSum(nums, i, res)
        return res

    # brute force
    def threeSumV1(self, nums: List[int]) -> List[List[int]]:
        sz = len(nums)
        out = []
        visited = {}
        nums = sorted(nums)

        for i in range(sz):
            for j in range(i + 1, sz):
                needed = -(nums[i] + nums[j])
                for k in range(j + 1, sz):
                    if nums[k] > needed:
                        break
                    if nums[k] != needed:
                        continue
                    triple = (nums[i], nums[j], nums[k])
                    if sum(triple) == 0:
                        if nums[i] not in visited:
                            visited[nums[i]] = set()
                        if nums[j] in visited[nums[i]]:
                            continue
                        out.append(triple)
                        visited[nums[i]].add(nums[j])

        return out
