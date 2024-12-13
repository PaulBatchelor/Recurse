# 2024-12-13: Mixture of a weighted directional graph
# algorithm and backtracking. This is what I came up with,
# I'm too tired to look up a better solution.
class Solution:
    def solveQuery(self, query, adj):
        # is there a path query(a,b) a => b?
        # look at each outgoing node from A, called x
        # now we ask if there's a path x => b?
        res = -1
        visited = set()
        def backtrack(node, target, path = []):
            nonlocal res, adj
            if node == target:
                res = 1
                for p in path:
                    res *= p
                return
            for candidate in adj[node]:
                value, weight = candidate
                if value in visited:
                    continue
                visited.add(value)
                path.append(weight)
                backtrack(value, target, path)
                path.pop()
        if query[0] not in adj or query[1] not in adj:
            return -1
        backtrack(query[0], query[1])
        return res

    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        adj = defaultdict(list)
        for i in range(len(equations)):
            eq = equations[i]
            val = values[i]
            left, right = eq
            if left not in adj:
                adj[left].append((left, 1.0))
            if right not in adj:
                adj[right].append((right, 1.0))
            adj[left].append((right, val))
            adj[right].append((left, 1.0/val))

        ret = []
        for query in queries:
            ret.append(self.solveQuery(query, adj))

        return ret


# a / b = 2
# a = 2b

# b = a / 2

# b / c = 3
# b = 3c
# c = b / 3

# b (1/2)=> a
# a (2)=> b
# b (3)=> c
# c (1/3) => b

# a / c, a (x)=> c

# a (?)=>c
# a (2)=> b (3)=> c

# b (?)=> a
# b (1/2) => a
