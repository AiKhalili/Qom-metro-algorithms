class UnionFind:
    """Disjoint Set structure with path compression and union by rank."""

    def __init__(self, elements):
        self._parent = {element: element for element in elements}
        self._rank = {element: 0 for element in elements}

    def find(self, x):
        """Return the representative of x's set."""

        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x, y):
        """Merge two sets; return False if they are already connected."""

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # already connected so would form a cycle

        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x

        self._parent[root_y] = root_x
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1

        return True

    def connected(self, x, y):
        """Return True if x and y are in the same set."""

        return self.find(x) == self.find(y)
