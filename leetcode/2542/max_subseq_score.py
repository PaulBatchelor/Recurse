# I struggled a lot with this problem. Then I struggled
# trying to understand the answer. Taking the morning
# now to implement the answer.
# I was close in my guess. The key piece missing from
# my intuition was sorting the nums2 array, and then
# keeping track of pairs in a new array.

from pprint import pprint
import heapq

def max_subseq_score(nums1, nums2, k):
    # create pairs array
    pairs = []
    h = []
    heapq.heapify(h)

    for i in range(0, len(nums1)):
        pairs.append([nums1[i], nums2[i]])

    # pairs needs to be sorted in descreasing order by
    # the second element. I don't know how to do that

    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    for i in range(0, k):
        heapq.heappush(h, pairs[i][0])

    pprint(pairs)
    top_k_sum = sum(h[0:3])
    answer = top_k_sum * pairs[k - 1][1]

    for i in range(k, len(nums1)):
        top_k_sum -= heapq.heappop(h)
        top_k_sum += pairs[i][0]
        heapq.heappush(h, pairs[i][0])
        answer = max(top_k_sum * pairs[i][1], answer)

    return answer

out = max_subseq_score([1, 3, 3, 2], [2, 1, 3, 4], 3)
print(out)
assert(out == 12)
