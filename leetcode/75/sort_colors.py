# 2024-10-14 this is the silly way. the follow-up wants
# you to do it in a single pass using constant extra space
# I looked up hints on claude, and it involves throwing
# things into bins.

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        nred = 0
        nwhite = 0
        nblue = 0

        for n in range(len(nums)):
            color = nums[n]
            if color == 0:
                nred += 1
            elif color == 1:
                nwhite  += 1
            elif color == 2:
                nblue += 1
            
        idx = 0
        for _ in range(nred):
            nums[idx] = 0
            idx+=1
        
        for _ in range(nwhite):
            nums[idx]= 1
            idx+=1
        
        for _ in range(nblue):
            nums[idx] = 2
            idx+=1
