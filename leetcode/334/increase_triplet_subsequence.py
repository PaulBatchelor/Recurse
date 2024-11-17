# 2024-11-17: Taken from editorial. I did not grok this
# problem well and gave up quickly.
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        first_num = second_num = 1 << 31
        for n in nums:
            if n <= first_num:
                first_num = n
            elif n <= second_num:
                second_num = n
            else:
                return True
        return False
