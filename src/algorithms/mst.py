import heapq


class MinimumSpanningTree:
    """T2.1: Find a minimum spanning tree using Prim's algorithm."""

    def __init__(self, graph):
        self.graph = graph

    def prim(self, start=None):
        """Return the MST edges and their total weight."""

        stations = self.graph.get_stations()
        if not stations:
            return [], 0

        if start is None:
            start = stations[0]
        elif not self.graph.has_station(start):
            raise ValueError(f"Station '{start}' does not exist.")

        visited = {start}
        selected = []
        total_cost = 0
        candidate_edges = []

        for edge in self.graph.get_neighbors(start):
            heapq.heappush(
                candidate_edges, (edge.weight, start, edge.destination, edge)
            )

        while candidate_edges and len(visited) < len(stations):
            weight, from_station, to_station, edge = heapq.heappop(candidate_edges)

            if to_station in visited:
                continue

            visited.add(to_station)

            selected.append(
                {
                    "from": from_station,
                    "to": to_station,
                    "distance": edge.distance,
                    "time": edge.time,
                    "weight": weight,
                }
            )

            total_cost += weight

            for next_edge in self.graph.get_neighbors(to_station):
                next_station = next_edge.destination

                if next_station not in visited:
                    heapq.heappush(
                        candidate_edges,
                        (next_edge.weight, to_station, next_station, next_edge),
                    )

        if len(visited) != len(stations):
            raise ValueError("The graph is disconnected; MST does not exist.")

        return selected, total_cost
