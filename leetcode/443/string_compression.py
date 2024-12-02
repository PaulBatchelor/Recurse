# 2024-12-02: I did solve it. The editorial solution was
# also a little tricky to get correct too.
class Solution:
    # editorial
    def compress(self, chars: List[str]) -> int:
        size = 0
        i = 0
        while i < len(chars):
            group_size = 1
            while (i + group_size) < len(chars) and chars[i + group_size] == chars[i]:
                group_size += 1
            chars[size] = chars[i]
            size += 1
            if group_size > 1:
                strnum = str(group_size)
                chars[size:size+len(strnum)] = list(strnum)
                size += len(strnum)
            i += group_size

        return size

    # kinda works, not clever though
    def compressV2(self, chars: List[str]) -> int:
        writepos = 0
        pos = 0
        last = 0
        while pos <= len(chars):
            if pos == len(chars):
                nchars = pos - last
                if nchars > 1:
                    for n in str(nchars):
                        writepos += 1
                        chars[writepos] = n
                pos += 1
                continue

            if chars[writepos] != chars[pos]:
                print(writepos, pos)
                nchars = pos - last
                last = pos
                if nchars > 1:
                    for n in str(nchars):
                        writepos += 1
                        chars[writepos] = n
                writepos += 1
                chars[writepos] = chars[pos]
            pos += 1

        return writepos + 1
