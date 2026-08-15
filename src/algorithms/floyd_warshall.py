class AllPairsShortestPath:
    """Compute all-pairs shortest paths using Floyd-Warshall."""

    VALID_CRITERIA = ("distance", "time")

    def __init__(self, graph):
        self.graph = graph
        self._criterion = None
        self._stations = []
        self._index = {}
        self._dist = []
        self._next = []

    def precompute(self, criterion="distance"):
        """Compute and cache the shortest-path matrix."""
        if criterion not in self.VALID_CRITERIA:
            raise ValueError(
                f"criterion must be one of {self.VALID_CRITERIA}, got '{criterion}'"
            )

        stations = self.graph.get_stations()
        n = len(stations)
        index = {station: i for i, station in enumerate(stations)}

        INF = float("inf")
        dist = [[INF] * n for _ in range(n)]
        next_hop = [[None] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0
            next_hop[i][i] = i

        for station in stations:
            u = index[station]
            for edge in self.graph.get_neighbors(station):
                v = index[edge.destination]
                weight = getattr(edge, criterion)

                if weight < dist[u][v]:
                    dist[u][v] = weight
                    next_hop[u][v] = v

        for k in range(n):
            for i in range(n):
                if dist[i][k] == INF:
                    continue

                dist_ik = dist[i][k]

                for j in range(n):
                    if dist[k][j] == INF:
                        continue

                    through_k = dist_ik + dist[k][j]

                    if through_k < dist[i][j]:
                        dist[i][j] = through_k
                        next_hop[i][j] = next_hop[i][k]

        self._criterion = criterion
        self._stations = stations
        self._index = index
        self._dist = dist
        self._next = next_hop

    def shortest_distance(self, start, end):
        """Return the cached shortest distance/time between two stations."""
        self._ensure_precomputed()
        self._validate_station(start)
        self._validate_station(end)

        i, j = self._index[start], self._index[end]
        value = self._dist[i][j]

        return value if value != float("inf") else None

    def shortest_path(self, start, end):
        """Return the cached shortest path between two stations."""
        self._ensure_precomputed()
        self._validate_station(start)
        self._validate_station(end)

        i, j = self._index[start], self._index[end]

        if self._next[i][j] is None:
            return None

        path_indices = [i]

        while i != j:
            i = self._next[i][j]
            path_indices.append(i)

        return [self._stations[idx] for idx in path_indices]

    def get_full_matrix(self):
        """Return the station order and cached shortest-path matrix."""
        self._ensure_precomputed()
        return self._stations, self._dist

    def _ensure_precomputed(self):
        if self._criterion is None:
            raise RuntimeError(
                "precompute() must be called before querying AllPairsShortestPath."
            )

    def _validate_station(self, station):
        if station not in self._index:
            raise ValueError(f"Station '{station}' does not exist.")
