class CriticalStations:
    """T4.3: Find articulation points and bridges in the (undirected)
    metro network using a DFS-based algorithm (Tarjan's method).

    Assumes the graph is undirected, i.e. every connection was added
    with directed=False so it appears symmetrically in both adjacency
    lists, as is the case for the shared Qom metro graph.
    """

    def __init__(self, graph):
        self.graph = graph
        self._computed = False
        self._articulation_points = set()
        self._bridges = []

    def analyze(self):
        """Run the DFS-based analysis and cache the results."""
        self._discovery = {}
        self._low = {}
        self._timer = 0
        self._articulation_points = set()
        self._bridges = []

        for station in self.graph.get_stations():
            if station not in self._discovery:
                self._dfs(station, parent=None)

        self._computed = True

    def _dfs(self, u, parent):
        self._discovery[u] = self._low[u] = self._timer
        self._timer += 1

        children = 0
        skip_one_parent_edge = True

        for edge in self.graph.get_neighbors(u):
            v = edge.destination

            if v == parent and skip_one_parent_edge:
                # allow re-visiting the parent only once, in case there
                # is a genuine second (parallel) edge between u and parent
                skip_one_parent_edge = False
                continue

            if v in self._discovery:
                # back edge to an already visited station
                self._low[u] = min(self._low[u], self._discovery[v])
            else:
                children += 1
                self._dfs(v, u)
                self._low[u] = min(self._low[u], self._low[v])

                if parent is not None and self._low[v] >= self._discovery[u]:
                    self._articulation_points.add(u)

                if self._low[v] > self._discovery[u]:
                    self._bridges.append(self._canonical_edge(u, v))

        if parent is None and children > 1:
            self._articulation_points.add(u)

    @staticmethod
    def _canonical_edge(u, v):
        """Return the edge as a sorted tuple so undirected duplicates match."""
        return tuple(sorted((u, v)))

    def get_articulation_points(self):
        """Return the list of stations whose removal disconnects the network."""
        self._ensure_computed()
        return sorted(self._articulation_points)

    def get_bridges(self):
        """Return the list of connections whose removal disconnects the network."""
        self._ensure_computed()
        return list(self._bridges)

    def is_articulation_point(self, station):
        """Return True if the given station is an articulation point."""
        self._ensure_computed()
        self._validate_station(station)
        return station in self._articulation_points

    def _ensure_computed(self):
        if not self._computed:
            raise RuntimeError(
                "analyze() must be called before querying CriticalStations."
            )

    def _validate_station(self, station):
        if not self.graph.has_station(station):
            raise ValueError(f"Station '{station}' does not exist.")
