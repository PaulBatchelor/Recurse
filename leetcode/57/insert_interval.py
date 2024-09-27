from pprint import pprint

def insert_interval(intervals, new_interval):
    out = []
    ni = new_interval
    start = 0
    end = 0

    for i in range(1, len(intervals)):
        if ni[0] >= intervals[i - 1][0]:
            start = i - 1
        if ni[1] < intervals[i][0]:
            end = i
    
    for i in range(0, len(intervals)):
        if i > start and i < end:
            continue
        elif i == start:
            iv = [intervals[start][0], max(intervals[end - 1][1], ni[1])]
            out.append(iv)
        else:
            out.append(intervals[i])

    print(start, end)
    return out

rc = insert_interval([[1, 3], [6, 9]], [2, 5])
assert(rc == [[1, 5], [6, 9]])

rc = insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8])
assert(rc == [[1, 2], [3, 10], [12, 16]])
