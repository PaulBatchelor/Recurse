class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        node = head
        sz = 0
        last = head

        # first pass to get the size
        while node:
            sz += 1
            last = node
            node = node.next

        removed_parent = sz - n - 1

        pos = 0

        # edge case: what if head changes?
        if removed_parent < 0:
            return head.next

        node = head
        while node:
            #print(pos, node.val)
            if pos == removed_parent:
                if node.next:
                    node.next = node.next.next
                else:
                    node.next = None
            pos += 1
            node = node.next

        return head
