# 2024-12-02

class Solution:
    def trim_spaces(self, s:str) -> list:
        left, right = 0, len(s) - 1
        while left <= right and s[left] == ' ':
            left += 1

        while left <= right and s[right] == ' ':
            right -= 1

        output = []
        while left <= right:
            if s[left] != ' ':
                output.append(s[left])
            elif output[-1] != ' ':
                output.append(s[left])
            left += 1

        return output
    def reverse(self, lst: list, left: int, right: int) -> None:
        while left < right:
            lst[left], lst[right] = lst[right], lst[left]
            left, right = left + 1, right - 1

    def reverse_each_word(self, lst: list) -> None:
        n = len(lst)
        start = end = 0
        while start < n:
            while end < n and lst[end] != ' ':
                end += 1

            self.reverse(lst, start, end - 1)
            start = end + 1
            end += 1

    def reverseWords(self, s:str) -> str:
        lst = self.trim_spaces(s)

        self.reverse(lst, 0, len(lst) - 1)

        self.reverse_each_word(lst)

        return "".join(lst)

    def reverseWords_builtin(self, s: str) -> str:
        return ' '.join(reversed(s.split()))
    # just some built-in stuff
    def reverseWordsV1(self, s: str) -> str:
        words = s.split(' ')
        words = filter(lambda s: len(s) > 0, words)
        words = list(words)
        return " ".join(list(reversed(words)))
