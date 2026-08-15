from data_structures.union_find import UnionFind


class KruskalMST:
    """Kruskal's MST algorithm using Union-Find for cycle detection."""

    def __init__(self, graph):
        self.graph = graph

    def kruskal(self):
        """
        Return the selected connections and total MST cost.
        Raise ValueError if the graph is disconnected.
        """

        stations = self.graph.get_stations()
        if not stations:
            return [], 0

        connections = sorted(
            self.graph.get_all_connections(), key=lambda c: c["weight"]
        )

        union_find = UnionFind(stations)
        selected = []
        total_cost = 0
        target_edge_count = len(stations) - 1

        for connection in connections:
            a, b = connection["from"], connection["to"]
            if union_find.union(a, b):
                selected.append(connection)
                total_cost += connection["weight"]

                if len(selected) == target_edge_count:
                    break  # tree is complete, no need to scan remaining edges

        if len(selected) != target_edge_count:
            raise ValueError("The graph is disconnected; MST does not exist.")

        return selected, total_cost
