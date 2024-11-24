# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    # fed into claude
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = out = ListNode()

        while list1 and list2:
            if list1.val <= list2.val: out.next, list1 = list1, list1.next
            else: out.next, list2 = list2, list2.next
            out = out.next

        out.next = list1 or list2
        return dummy.next

    # peeked at solution to loook for ways to clean it up
    def mergeTwoListsV2(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        out = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                out.next = list1
                list1 = list1.next
            else:
                out.next = list2
                list2 = list2.next
            out = out.next

        out.next = list1 if list1 else list2

        return dummy.next

    def mergeTwoListsV1(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        out = dummy

        while list1 or list2:
            # if any of the two lists are empty, just append the other list
            if not list1:
                out.next = list2
                list2 = list2.next
            elif not list2:
                out.next = list1
                list1 = list1.next
            # otherwise, append the smallest value
            elif list1.val < list2.val:
                out.next = list1
                list1 = list1.next
            else:
                out.next = list2
                list2 = list2.next
            out = out.next

        return dummy.next
