# 2024-11-23: The solution came together pretty intuitively,
# especially since working on similar problems like
# maximum subarray. I wish I could explain why it works.
# INterestingly, the claude code-golfed solution is slower,
# most likely because it makes calls to min/max every loop
# while my version has conditions in place to minimize
# those calls

class Solution:
    # code golf answer from claude, it's slower, probably
    # because of the two calls to min/max
    def maxProfit(self, prices: List[int]) -> int:
        min_price = inf
        max_profit = 0

        for price in prices:
            min_price = min(price, min_price)
            max_profit = max(max_profit, price - min_price)

        return max_profit

    # this is my answer
    def maxProfitV1(self, prices: List[int]) -> int:
        min_so_far = inf
        max_profit = 0
        for price in prices:
            if price < min_so_far:
                min_so_far = price
                continue
            max_profit = max(max_profit, price - min_so_far)

        return max_profit
