# 2024-11-28 I am starting to see the craft now. I hack
# and slashed and stumbled my way through my solution.
# there's nothing terribly clever, but you can be organized
# about it.
oclass Solution:
    # adopted from editorial, what I did but cleaner
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        for i in range(len(flowerbed)):
            if flowerbed[i] == 1:
                continue
            empty_left = (i == 0) or (flowerbed[i - 1] == 0)
            empty_right = (i == len(flowerbed) - 1) or (flowerbed[i + 1] == 0)

            if empty_left and empty_right:
                flowerbed[i] = 1
                n -= 1

        return n <= 0

    # hack and slash version quickly coded up
    def canPlaceFlowersV1(self, flowerbed: List[int], n: int) -> bool:
        if n == 0:
            return True
        if len(flowerbed) == 1:
            if n > 1:
                return False
            if flowerbed[0] == 0:
                return True
        for i in range(len(flowerbed)):
            if flowerbed[i] == 1:
                continue

            if i == 0 and flowerbed[i + 1] == 0:
                flowerbed[i] = 1
                n -= 1
                continue

            if i == len(flowerbed) - 1 and flowerbed[i - 1] == 0:
                flowerbed[i] = 1
                n -= 1
                continue

            if flowerbed[i - 1] == 0 and flowerbed[i + 1] == 0:
                flowerbed[i] = 1
                n -= 1

        return n <= 0
