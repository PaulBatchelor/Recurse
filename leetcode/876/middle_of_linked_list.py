# 2024-11-26 I knew the solution involved slow/fast pointer,
# but couldn't quick get the logic worked out. The
# trick is this: the difference between the fast pointer
# list in (1 2 3 4 5) and (1 2 3 4 5 6) is (1 3 5) and
# (1 3 5 NULL). Note the NULL.

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    # editorial fast/slow pointer solution
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow

    # worked out with my own logic
    def middleNodeV1(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        if head.next is None:
            return head

        slow = head
        fast = head.next

        while fast and fast.next:
            fast = fast.next.next
            if not fast:
                break
            slow = slow.next

        return slow.next

# 1 2 3 4 5
# 1 3 5
# 1 2 3

# 1 2 3 4 5 6
# 1 3 5 NULL
# 1 2 3 4
