from collections import deque, defaultdict


class MaxFlow:
    """T4.2: Compute maximum passenger flow between two stations
    using the Edmonds-Karp algorithm (Ford-Fulkerson with BFS)."""

    def __init__(self, graph):
        self.graph = graph

    def find_max_flow(self, source, sink):
        """Return the maximum flow value and the flow carried on each edge."""

        if not self.graph.has_station(source):
            raise ValueError(f"Station '{source}' does not exist.")
        if not self.graph.has_station(sink):
            raise ValueError(f"Station '{sink}' does not exist.")
        if source == sink:
            raise ValueError("Source and sink must be different stations.")

        capacity, adjacency = self._build_flow_network()
        residual = dict(capacity)

        max_flow_value = 0

        while True:
            path = self._bfs_augmenting_path(residual, adjacency, source, sink)
            if path is None:
                break

            bottleneck = min(residual[(u, v)] for u, v in zip(path, path[1:]))

            for u, v in zip(path, path[1:]):
                residual[(u, v)] -= bottleneck
                residual[(v, u)] += bottleneck

            max_flow_value += bottleneck

        flow_per_edge = self._extract_flow(capacity, residual)

        return max_flow_value, flow_per_edge

    def _build_flow_network(self):
        """Build a directed capacity map and adjacency sets from the graph.

        Every edge (including undirected ones stored twice by Graph)
        contributes its capacity in its own direction; a zero-capacity
        reverse arc is registered wherever it is missing, so the
        residual graph can always push flow back.
        """
        capacity = {}
        adjacency = defaultdict(set)

        for station in self.graph.get_stations():
            adjacency.setdefault(station, set())
            for edge in self.graph.get_neighbors(station):
                u, v = station, edge.destination
                edge_capacity = edge.capacity if edge.capacity is not None else 0

                capacity[(u, v)] = capacity.get((u, v), 0) + edge_capacity
                capacity.setdefault((v, u), 0)

                adjacency[u].add(v)
                adjacency[v].add(u)

        return capacity, adjacency

    def _bfs_augmenting_path(self, residual, adjacency, source, sink):
        """Find the shortest (fewest-edges) augmenting path with residual capacity."""

        parent = {source: None}
        queue = deque([source])

        while queue:
            current = queue.popleft()
            if current == sink:
                break

            for neighbor in adjacency[current]:
                if neighbor in parent:
                    continue
                if residual[(current, neighbor)] <= 0:
                    continue
                parent[neighbor] = current
                queue.append(neighbor)

        if sink not in parent:
            return None

        return self._reconstruct_path(parent, sink)

    @staticmethod
    def _reconstruct_path(parent, sink):
        """Reconstruct the path using the parent mapping."""
        path = []
        node = sink
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path

    @staticmethod
    def _extract_flow(capacity, residual):
        """Return only the real arcs (original capacity > 0) that carry flow."""
        flow = {}
        for (u, v), cap in capacity.items():
            if cap <= 0:
                continue
            used = cap - residual[(u, v)]
            if used > 0:
                flow[(u, v)] = used
        return flow
