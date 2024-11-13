# 2024-11-13: Greedy algorithm, adapted from https://www.youtube.com/watch?v=lJwbPZGo05A
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost):
            return -1
        total = 0
        found = 0
        for i in range(len(gas)):
            total += gas[i] - cost[i]
            if total < 0:
                total = 0
                found = i + 1

        return found
