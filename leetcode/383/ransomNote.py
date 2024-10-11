from collections import Counter
class Solution:
    # claude optimization: uses specialized Counter type,
    # which is a dict subclass. Much more performant
    def canConstructV2(self, ransomNote: str, magazine: str) -> bool:
        ran_count = Counter(ransomNote)
        mag_count = Counter(magazine)

        for char, count in ran_count.items():
            if mag_count[char] < count:
                return False   

        return True


    # my initial solution: uses vanilla python dicts.
    def canConstructV1(self, ransomNote: str, magazine: str) -> bool:
        mag_map = {}
        ran_map = {}

        for s in magazine:
            if s in mag_map:
                mag_map[s] += 1
            else:
                mag_map[s] = 1

        for s in ransomNote:
            if s not in mag_map:
                return False

            if s in ran_map:
                ran_map[s] += 1
            else:
                ran_map[s] = 1
        
        for s in ransomNote:
            if mag_map[s] < ran_map[s]:
                return False
        
        return True
