import heapq


class ShortestPath:
    """T1.3: Find shortest paths using Dijkstra's algorithm."""

    VALID_CRITERIA = ("distance", "time")

    def __init__(self, graph):
        self.graph = graph

    def find_shortest_path(self, start, end, criterion="distance"):
        """Return the shortest path and its total distance or travel time."""

        if criterion not in self.VALID_CRITERIA:
            raise ValueError(
                f"criterion must be one of {self.VALID_CRITERIA}, got '{criterion}'"
            )
        if not self.graph.has_station(start):
            raise ValueError(f"Station '{start}' does not exist.")
        if not self.graph.has_station(end):
            raise ValueError(f"Station '{end}' does not exist.")

        if start == end:
            return [start], 0

        best_cost = {start: 0}
        parent = {start: None}
        visited = set()
        priority_queue = [(0, start)]

        while priority_queue:
            current_cost, current = heapq.heappop(priority_queue)

            if current in visited:
                continue
            visited.add(current)

            if current == end:
                break

            for edge in self.graph.get_neighbors(current):
                neighbor = edge.destination
                if neighbor in visited:
                    continue

                new_cost = current_cost + getattr(edge, criterion)

                if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                    best_cost[neighbor] = new_cost
                    parent[neighbor] = current
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        if end not in best_cost:
            return None, None

        return self._reconstruct_path(parent, end), best_cost[end]

    @staticmethod
    def _reconstruct_path(parent, end):
        """Reconstruct the path from the parent mapping."""

        path = []
        node = end
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path
