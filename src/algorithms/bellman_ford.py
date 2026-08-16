class BellmanFord:
    """T2.4: Bellman-Ford with negative-cycle detection."""

    VALID_CRITERIA = ("distance", "time", "weight")

    def __init__(self, graph):
        self.graph = graph

    def _all_edges(self):
        return [
            (station, edge)
            for station in self.graph.get_stations()
            for edge in self.graph.get_neighbors(station)
        ]

    def _validate_criterion(self, criterion):
        if criterion not in self.VALID_CRITERIA:
            raise ValueError(
                f"criterion must be one of {self.VALID_CRITERIA}, " f"got '{criterion}'"
            )

    def _relax_from_virtual_source(self, criterion):
        """Check the whole graph for a negative cycle."""
        stations = self.graph.get_stations()
        edges = self._all_edges()

        distance = {station: 0 for station in stations}
        parent = {station: None for station in stations}

        cycle_node = None

        for i in range(len(stations)):
            updated = False

            for u, edge in edges:
                v = edge.destination
                edge_cost = getattr(edge, criterion)

                new_cost = distance[u] + edge_cost

                if new_cost < distance[v]:
                    distance[v] = new_cost
                    parent[v] = u
                    updated = True

                    if i == len(stations) - 1:
                        cycle_node = v

            if not updated:
                break

        return distance, parent, cycle_node

    def has_negative_cycle(self, criterion="weight"):
        """Return True if a negative-weight cycle exists."""
        self._validate_criterion(criterion)

        _, _, cycle_node = self._relax_from_virtual_source(criterion)

        return cycle_node is not None

    def find_negative_cycle(self, criterion="weight"):
        """Return a negative cycle, or None if there is no such cycle."""
        self._validate_criterion(criterion)

        stations = self.graph.get_stations()
        _, parent, cycle_node = self._relax_from_virtual_source(criterion)

        if cycle_node is None:
            return None

        node = cycle_node

        for _ in range(len(stations)):
            node = parent[node]

        cycle = [node]
        current = parent[node]

        while current != node:
            cycle.append(current)
            current = parent[current]

        cycle.append(node)
        cycle.reverse()

        return cycle

    def shortest_path(self, start, end, criterion="weight"):
        """Return the shortest path and its cost."""
        self._validate_criterion(criterion)

        if not self.graph.has_station(start):
            raise ValueError(f"Station '{start}' does not exist.")

        if not self.graph.has_station(end):
            raise ValueError(f"Station '{end}' does not exist.")

        if self.has_negative_cycle(criterion):
            raise ValueError(
                "The graph contains a negative-weight cycle; "
                "shortest paths are undefined."
            )

        if start == end:
            return [start], 0

        stations = self.graph.get_stations()
        edges = self._all_edges()

        infinity = float("inf")

        distance = {station: infinity for station in stations}
        parent = {station: None for station in stations}

        distance[start] = 0

        for _ in range(len(stations) - 1):
            updated = False

            for u, edge in edges:
                v = edge.destination

                if distance[u] == infinity:
                    continue

                edge_cost = getattr(edge, criterion)
                new_cost = distance[u] + edge_cost

                if new_cost < distance[v]:
                    distance[v] = new_cost
                    parent[v] = u
                    updated = True

            if not updated:
                break

        if distance[end] == infinity:
            return None, None

        return self._reconstruct_path(parent, end), distance[end]

    @staticmethod
    def _reconstruct_path(parent, end):
        path = []
        node = end

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path
