# 2024-12-06: Had to work through convincing myself that
# this logic was sound. Also needed to review and make
# sure counters worked the way I expected
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        w1counts = Counter(word1)
        w2counts = Counter(word2)

        # make sure they have the same set of words

        same_set = w1counts.keys() == w2counts.keys()

        # any swaps that occur, the count profile will remain
        # the same

        same_counts = sorted(w1counts.values()) == sorted(w2counts.values())

        return same_set and same_counts
