# valid anagram:
# approach 1: compare count maps of s and t
# approach 2: sort and compare strings

def valid_anagram_v1(str1, str2):
    counts1 = {}
    counts2 = {}

    if len(str1) != len(str2):
        return False

    for s in str1:
        if s not in counts1:
            counts1[s] = 1
        else:
            counts1[s] += 1

    for s in str2:
        if s not in counts2:
            counts2[s] = 1
        else:
            counts2[s] += 1

    for k in counts1.keys():
        if k not in counts2 or counts2[k] != counts1[k]:
            return False

    return True

def valid_anagram_v2(str1, str2):
    str1 = ''.join(sorted(str1))
    str2 = ''.join(sorted(str2))
    return str1 == str2

def test(f):
    rc = f("anagram", "nagaram")
    assert(rc)
    rc = f("rat", "car")
    assert(not rc)

test(valid_anagram_v1)
test(valid_anagram_v2)
