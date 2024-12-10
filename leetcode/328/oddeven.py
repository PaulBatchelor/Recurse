# 2024-12-10: in my first version, I didn't piece together
# that even was the only value needed to be tracked.
# linking logic is hard.
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        odd = head
        even = head.next
        even_head = even

        while even and even.next:
            odd.next = even.next
            odd = odd.next

            even.next = odd.next
            even = even.next

        odd.next = even_head
        return head
    def oddEvenListV1(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None

        odd = head
        even = head.next
        even_head = even

        # relink nodes
        while odd and even:
            odd.next = even.next
            if odd.next is None:
                odd.next = even_head
                return head
            odd = odd.next
            even.next = odd.next if odd else None
            even = even.next

            #even.next = even.next.next
        # link last value at the end
        odd.next = even_head
        return head


