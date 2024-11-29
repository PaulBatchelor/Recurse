# 2024-11-28: yup. that's how you do it. pleased I
# remembered how to do the swap trick. I keep forgetting
# strings need to be converted to lists and joined again
class Solution:
    def reverseVowels(self, s: str) -> str:
        s = list(s)
        left = 0
        right = len(s) - 1
        vowels="aeiouAEIUO"
        while left < right:
            if s[left] not in vowels:
                left += 1
                continue
            if s[right] not in vowels:
                right -= 1
                continue

            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
        return "".join(s)
