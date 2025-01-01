# 2025-01-01: Got the top down solution correct, read
# the editorial to look up bottoms up and bottoms up
# space optimized approaches
class Solution:
    # bottoms up, space optimized
    def deleteAndEarn(self, nums: List[int]) -> int:
        points = defaultdict(int)
        max_number = 0

        for num in nums:
            points[num] += num
            max_number = max(num, max_number)

        two_back = 0
        one_back = points[1]

        for i in range(2, max_number + 1):
            #max_points[i] = max(max_points[i - 1], max_points[i - 2] + points[i])
            tmp = max(one_back, two_back + points[i])
            two_back = one_back
            one_back = tmp

        return one_back

    # bottoms up
    def deleteAndEarnV3(self, nums: List[int]) -> int:
        points = defaultdict(int)
        max_number = 0
        for num in nums:
            points[num] += num
            max_number = max(num, max_number)

        max_points = [0] * (max_number + 1)
        max_points[1] = points[1]

        for i in range(2, max_number + 1):
            max_points[i] = max(max_points[i - 1], max_points[i - 2] + points[i])

        return max_points[max_number]

    # top-down, based on editorial
    def deleteAndEarnV2(self, nums: List[int]) -> int:
        points = defaultdict(int)
        max_number = 0

        for num in nums:
            points[num] += num
            max_number = max(num, max_number)

        def max_points(num):
            if num == 0:
                return 0
            if num == 1:
                return points[1]

            if num not in memo:
               memo[num] = max(max_points(num - 1), max_points(num - 2) + points[num])
            return memo[num]


        memo = {}
        return max_points(max_number)


    def deleteAndEarnV1(self, nums: List[int]) -> int:
        counts = Counter(nums)
        maxnum = max(nums)
        minnum = min(nums)
        def dp(i):
            if i < minnum or i > maxnum:
                return 0

            if i not in memo:
                n = counts[i] if i in counts else 0
                take_it = i * n + dp(i - 2)
                dont_take_it = dp(i - 1)
                memo[i] = max(take_it, dont_take_it)

            return memo[i]

        memo = {}

        return dp(maxnum)


