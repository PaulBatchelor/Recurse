class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        h = defaultdict(int)

        count = 0
        psum = 0
        for num in nums:
            psum += num

            if psum == k:
                count += 1

            count += h[psum - k]
            h[psum] += 1

        return count
