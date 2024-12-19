# 2024-12-19: figured out a solution, the editorial makes
# use of the bisect module, which I never used before.
# also the trick of using the integer divide with
# (success * (x - 1)//x) was a bit clever
class Solution:
    # editorial
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        answer = []
        m = len(potions)
        maxPotion = potions[m - 1]

        for spell in spells:
            minPotion = (success + spell - 1) // spell
            if minPotion > maxPotion:
                answer.append(0)
                continue
            index = bisect.bisect_left(potions, minPotion)
            answer.append(m - index)

        return answer
    # my version (accepted)
    def successfulPairsV1(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions = sorted(potions)
        out = []
        nspells = len(spells)
        npotions = len(potions)

        for i in range(nspells):
            target = ceil(success / spells[i])
            left = 0
            right = npotions - 1
            if target > potions[npotions - 1]:
                out.append(0)
                continue
            while left < right:
                mid = left + (right - left) // 2
                if potions[mid] < target:
                    left = mid + 1
                else:
                    right = mid

            out.append(npotions - left)

        return out
