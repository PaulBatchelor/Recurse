from pprint import pprint

class LinkedList:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = None

def mklist(vals):
    dummy = LinkedList()
    entry = dummy
    for x in vals:
        entry.next = LinkedList(x)
        entry = entry.next
    return dummy.next

def to_array(lst):
    a = []
    entry = lst
    while (entry is not None):
        a.append(entry.val)
        entry = entry.next
    return a

def merge_sorted(list1, list2):
    node1 = list1
    node2 = list2
    dummy = LinkedList()
    curnode = dummy

    while node1 is not None or node2 is not None:
        # which one to choose next?
        if node1 is None:
            curnode.next = node2
            node2 = node2.next
        elif node2 is None:
            curnode.next = node1
            node1 = node1.next
        else:
            v1 = node1.val
            v2 = node2.val
            if v1 < v2:
                curnode.next = node1
                node1 = node1.next
            else:
                curnode.next = node2
                node2 = node2.next

        curnode = curnode.next
    return dummy.next

out = to_array(merge_sorted(mklist([1, 3, 4]), mklist([1, 2, 4])))
assert(out == [1, 1, 2, 3, 4, 4])

out = to_array(merge_sorted(mklist([]), mklist([])))
assert(out == [])

out = to_array(merge_sorted(mklist([]), mklist([0])))
assert(out == [0])
