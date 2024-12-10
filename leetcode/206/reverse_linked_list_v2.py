# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        node = head
        while node:
            next_node = node.next
            node.next = prev
            prev = node
            node = next_node
        return prev

    def reverseListV1(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        prev = None
        node = head
        while node is not None:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        return prev
