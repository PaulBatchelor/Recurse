# throwing distances in a heap of size K would be a good
# way to get the K closest distances, but how do we track
# the distances as they correspond to ID? hashmap of distance -> id
# I'm assuming the points are all integer values, and
# we can just store the squared values.

# The editorial for this one has two different approaches:
# sorting an array and choosing the top K values,
# and then some sort of divide and conquer

from pprint import pprint
import heapq

# use a maxheap to keep track of K smallest points,
# and a hashmap to map distances to indices
def k_closest_points(points, k):
    h = []
    heapq.heapify(h)
    lookup = {}
    for i in range(0, k):

        # wrong equation, should be add not subtract
        # origin is always 0,0, so it can be ignored
        # sqrt can be ignored as well because sqrt(x) < x
        # for all positive x
        # dist = \
        #     points[i][0]*points[i][0] - \
        #     points[i][1]*points[i][1]
        
        dist = \
            points[i][0]*points[i][0] + \
            points[i][1]*points[i][1]
        lookup[dist] = i
        # apparently it's standard procedure to negate values
        # to turn into max-heap?a
        # https://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python
        heapq.heappush(h, -dist)

    for i in range(k, len(points)):
        heapq.heappop(h)
        dist = \
            points[i][0]*points[i][0] - \
            points[i][1]*points[i][1]
        lookup[dist] = i
        heapq.heappush(h, -dist)

    out = []
    while (len(h) > 0):
        dist = heapq.heappop(h)
        out.append(points[lookup[-dist]])

    return out

def flattener(a):
    out = []
    for xy in a:
        out.extend(xy)

    return sorted(out)


def test(f):
    out = f([[1, 3], [-2, 2]], 1)
    expected = flattener([[-2, 2]])
    assert(flattener(out) == expected)

    out = f([[3, 3], [5, -1], [-2, 4]], 2)
    expected = flattener([[3, 3], [-2, 4]])
    assert(flattener(out) == expected)

# simple sort, solution 1 from editorial
def k_closest_points_sort(points, k):
    dists = []
    out = []
    for pt in points:
        dists.append(pt[0]*pt[0] + pt[1]*pt[1])

    dists = sorted(dists)
    kmax = dists[k - 1]
    for pt in points:
        dist = pt[0]*pt[0] + pt[1]*pt[1]
        if dist <= kmax:
            out.append(pt)

    return out


# TODO: figure out divide and conquer approach?
# this seems to use quickselect

test(k_closest_points)
test(k_closest_points_sort)
