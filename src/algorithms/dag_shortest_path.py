class DAGShortestPath:
    """
    T2.3: Shortest path in a Directed Acyclic Graph (DAG).

    Algorithm: topological sort (DFS) -> relax edges in that order ->
    reconstruct path from parent pointers.

    Must be used with a dedicated, directed Express Line graph
    (built with directed=True). Running it on the main, undirected
    metro graph will always raise a cycle error.
    """

    VALID_CRITERIA = ("distance", "time", "weight")

    def __init__(self, graph):
        self.graph = graph

    def topological_order(self):
        """
        Return stations in topological order via DFS.
        Raises ValueError if the graph contains a cycle.
        """
        stations = self.graph.get_stations()
        state = {}  # station -> "visiting" | "done"
        order = []

        def visit(station):
            state[station] = "visiting"
            for edge in self.graph.get_neighbors(station):
                neighbor_state = state.get(edge.destination)
                if neighbor_state == "visiting":
                    raise ValueError(
                        "The graph contains a cycle; it is not a valid DAG."
                    )
                if neighbor_state is None:
                    visit(edge.destination)
            state[station] = "done"
            order.append(station)

        for station in stations:
            if station not in state:
                visit(station)

        order.reverse()
        return order

    def shortest_path(self, start, end, criterion="distance"):
        """
        Return (path, cost) between start and end using distance,
        time, or weight as the edge cost. Returns (None, None) if
        end is unreachable. Raises ValueError for an invalid
        criterion, a missing station, or a cyclic graph.
        """
        if criterion not in self.VALID_CRITERIA:
            raise ValueError(
                f"criterion must be one of {self.VALID_CRITERIA}, got '{criterion}'"
            )
        if not self.graph.has_station(start):
            raise ValueError(f"Station '{start}' does not exist.")
        if not self.graph.has_station(end):
            raise ValueError(f"Station '{end}' does not exist.")

        # validated unconditionally (even for start == end) so a cycle
        # anywhere in the graph always raises, regardless of query
        order = self.topological_order()

        if start == end:
            return [start], 0

        infinity = float("inf")
        distance = {station: infinity for station in order}
        parent = {station: None for station in order}
        distance[start] = 0

        for station in order:
            if distance[station] == infinity:
                continue

            for edge in self.graph.get_neighbors(station):
                neighbor = edge.destination
                new_cost = distance[station] + getattr(edge, criterion)

                if new_cost < distance[neighbor]:
                    distance[neighbor] = new_cost
                    parent[neighbor] = station

        if distance[end] == infinity:
            return None, None

        return self._reconstruct_path(parent, end), distance[end]

    @staticmethod
    def _reconstruct_path(parent, end):
        """Reconstruct the path from the parent mapping."""
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path
