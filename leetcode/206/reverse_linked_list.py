# I'm trying to build intuition around the recursive
# solution.

class LinkedList:
    value = None
    next = None


elem = LinkedList()

def array_to_linked_list(arr):
    prev = None
    head = None
    for a in arr:
        elem = LinkedList()
        elem.value = a
        if prev != None:
            prev.next = elem
        else:
            head = elem
        prev = elem

    return head


def print_values(head):
    elem = head
    while (elem != None):
        print(elem.value)
        elem = elem.next

def recursive_reverse(head):
    if head == None or head.next == None:
        return head

    p = recursive_reverse(head.next)
    head.next.next = head
    head.next = None
    return p

ll = array_to_linked_list([1, 2, 3, 4, 5])

print_values(ll)

ll = recursive_reverse(ll)

print_values(ll)
