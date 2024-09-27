# this simplest way to solve this is to use recursion.
# so, that's what we'll do

from pprint import pprint

def flood_fill_rec(image, sr, sc, color, orig):
    # bounds checking
    if sr < 0 or sr >= len(image):
        return

    if sc < 0 or sc >= len(image[0]):
        return

    cur = image[sr][sc]

    if cur != orig:
        return

    image[sr][sc] = color

    # north
    flood_fill_rec(image, sr - 1, sc, color, orig)

    # south
    flood_fill_rec(image, sr + 1, sc, color, orig)

    # east
    flood_fill_rec(image, sr, sc + 1, color, orig)

    # west
    flood_fill_rec(image, sr, sc - 1, color, orig)

def flood_fill(image, sr, sc, color):
    flood_fill_rec(image, sr, sc, color, image[sr][sc])
    return image

out = flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2)
expected = [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
assert(out == expected)
