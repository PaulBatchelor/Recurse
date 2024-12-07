# 2024-12-07: I had some solution that worked (eventually),
# then I fed it into Claude to see what it would do.
# Definitely a details oriented problem

class Solution:
    # my approach, fed into claude, transcribed by hand
    def decodeString(self, s: str) -> str:
        stk = []

        for ch in s:
            # add characters until latest pattern added is closed
            if ch != ']':
                stk.append(ch)
                continue


            # extract substring of latest pattern
            substr = ''

            while stk[-1] != '[':
                # the ordering is needed here because of stack order
                # stack items can be previously evaluated patterns inside the current enclosign pattern
                substr = stk.pop() + substr

            # removes opening bracket
            stk.pop()

            # extract the number of reps
            nreps = ''
            while stk and stk[-1].isdigit():
                nreps = stk.pop() + nreps

            # append evaluated pattern to global stack
            stk.append(substr * int(nreps or 0))

        return "".join(stk)

    # my approach that I came up with
    def decodeStringV1(self, s: str) -> str:
        out = ""

        s = list(reversed(s))

        while s:
            ch = s.pop()
            # string is made up of chunks.
            # either they are strings or repeated patterns

            # simple string chunk only contains lowercase english
            # letters. Consume input until a non-alphabetic
            # character is found or end of string, and append
            # to output string
            while s and ch.isalpha():
                out += ch
                ch = s.pop() if s else None

            # repeated string is a number, a left bracket,
            # a pattern string, and then a closing right bracket
            # pattern matching turns into a matching bracket
            # problem, which can be solved using a stack

            if not s:
                out += ch
                break

            reps = '0'

            while s and ch.isnumeric():
                reps += ch
                ch = s.pop() if s else None

            stk = []
            stk.append(ch)
            pat = ch
            while s and stk:
                ch = s.pop()
                if ch == ']':
                    stk.pop()
                elif ch == '[':
                    stk.append(ch)
                pat += ch

            out += self.decodeString(pat[1:-1]) * int(reps)


        # return the output string
        return out
