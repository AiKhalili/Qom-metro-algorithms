from collections import deque


class Reachability:
    """T1.2: Find a valid path between two stations using BFS."""

    def __init__(self, graph):
        self.graph = graph

    def is_reachable(self, start, end):
        """Return True if a path exists between two stations."""
        return self.find_path(start, end) is not None

    def find_path(self, start, end):
        """Return one valid path from start to end, or None."""
        if not self.graph.has_station(start):
            raise ValueError(f"Station '{start}' does not exist.")
        if not self.graph.has_station(end):
            raise ValueError(f"Station '{end}' does not exist.")

        if start == end:
            return [start]

        visited = {start}
        parent = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            for edge in self.graph.get_neighbors(current):
                neighbor = edge.destination
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                parent[neighbor] = current
                if neighbor == end:
                    return self._reconstruct_path(parent, end)
                queue.append(neighbor)

        return None  # end was never reached so no path exists

    @staticmethod
    def _reconstruct_path(parent, end):
        """Reconstruct the path using the parent mapping."""
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path
