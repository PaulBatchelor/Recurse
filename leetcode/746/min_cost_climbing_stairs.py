# 2024-12-21: Working out the optimal substructure below
# with the test cases was helpful. Got me to realize
# the small memory solution.

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        s1 = cost[0]
        s2 = cost[1]

        for i in range(2, len(cost)):
            tmp = cost[i] + min(s1, s2)
            s1 = s2
            s2 = tmp

        return min(s1, s2)

# 10 15 20

# 10 15 30

# 1,100,1,1,1,100,1,1,100,1

# 1 100 2 3 3 103 4 5 104 6
