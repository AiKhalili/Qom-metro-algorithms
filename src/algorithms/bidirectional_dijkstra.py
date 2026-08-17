import heapq
from collections import defaultdict


class BidirectionalDijkstra:
    """Find shortest paths using bidirectional Dijkstra search."""

    VALID_CRITERIA = ("distance", "time")

    def __init__(self, graph):
        """Initialize the algorithm with the given graph."""

        self.graph = graph
        self._reverse_adjacency = self._build_reverse_adjacency()

    def _build_reverse_adjacency(self):
        """Build the reverse adjacency list of the graph."""

        reverse = defaultdict(list)

        for station in self.graph.get_stations():
            reverse[station] = []

        for conn in self.graph.get_all_connections():
            reverse[conn["to"]].append(
                {
                    "destination": conn["from"],
                    "distance": conn["distance"],
                    "time": conn["time"],
                }
            )
            if not conn["directed"]:
                reverse[conn["from"]].append(
                    {
                        "destination": conn["to"],
                        "distance": conn["distance"],
                        "time": conn["time"],
                    }
                )

        return reverse

    @staticmethod
    def _top_of(pq, dist, visited):
        """Return the smallest valid tentative distance in the queue."""

        while pq:
            cost, node = pq[0]
            if node in visited or cost != dist.get(node):
                heapq.heappop(pq)
            else:
                return cost
        return float("inf")

    def find_shortest_path(self, start, end, criterion="distance"):
        """Return the shortest path, cost, and expansion statistics."""

        if criterion not in self.VALID_CRITERIA:
            raise ValueError(
                f"criterion must be one of {self.VALID_CRITERIA}, got '{criterion}'"
            )
        if not self.graph.has_station(start):
            raise ValueError(f"Station '{start}' does not exist.")
        if not self.graph.has_station(end):
            raise ValueError(f"Station '{end}' does not exist.")

        if start == end:
            return [start], 0, {"nodes_expanded": 0}

        forward_dist = {start: 0}
        forward_parent = {start: None}
        forward_visited = set()
        forward_pq = [(0, start)]

        backward_dist = {end: 0}
        backward_parent = {end: None}
        backward_visited = set()
        backward_pq = [(0, end)]

        best_cost = float("inf")
        meeting_node = None
        nodes_expanded = 0

        def relax(pq, dist, parent, visited, current_cost, current, neighbors):
            """Relax outgoing edges from the current node."""

            for edge in neighbors:
                is_dict = isinstance(edge, dict)
                neighbor = edge["destination"] if is_dict else edge.destination
                weight = edge[criterion] if is_dict else getattr(edge, criterion)

                if weight < 0:
                    raise ValueError(
                        "BidirectionalDijkstra requires non-negative edge "
                        "weights; use Bellman-Ford for graphs with negative "
                        "weights (see T2.4)."
                    )

                if neighbor in visited:
                    continue

                new_cost = current_cost + weight
                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))

        while forward_pq and backward_pq:
            forward_top = self._top_of(forward_pq, forward_dist, forward_visited)
            backward_top = self._top_of(backward_pq, backward_dist, backward_visited)

            if forward_top == float("inf") or backward_top == float("inf"):
                break  # one side is exhausted; no path can be completed

            if forward_top + backward_top >= best_cost:
                break  # no undiscovered path can improve on best_cost

            # expand forward side
            f_cost, f_node = heapq.heappop(forward_pq)
            if f_node not in forward_visited and f_cost == forward_dist[f_node]:
                forward_visited.add(f_node)
                nodes_expanded += 1

                if f_node in backward_dist:
                    total = f_cost + backward_dist[f_node]
                    if total < best_cost:
                        best_cost = total
                        meeting_node = f_node

                relax(
                    forward_pq,
                    forward_dist,
                    forward_parent,
                    forward_visited,
                    f_cost,
                    f_node,
                    self.graph.get_neighbors(f_node),
                )

            # expand backward side
            b_cost, b_node = heapq.heappop(backward_pq)
            if b_node not in backward_visited and b_cost == backward_dist[b_node]:
                backward_visited.add(b_node)
                nodes_expanded += 1

                if b_node in forward_dist:
                    total = forward_dist[b_node] + b_cost
                    if total < best_cost:
                        best_cost = total
                        meeting_node = b_node

                relax(
                    backward_pq,
                    backward_dist,
                    backward_parent,
                    backward_visited,
                    b_cost,
                    b_node,
                    self._reverse_adjacency[b_node],
                )

        if meeting_node is None:
            return None, None, {"nodes_expanded": nodes_expanded}

        path = self._reconstruct_path(forward_parent, backward_parent, meeting_node)
        return path, best_cost, {"nodes_expanded": nodes_expanded}

    @staticmethod
    def _reconstruct_path(forward_parent, backward_parent, meeting_node):
        """Combine the forward and backward paths at the meeting node."""
        forward_path = []
        node = meeting_node
        while node is not None:
            forward_path.append(node)
            node = forward_parent[node]
        forward_path.reverse()

        backward_path = []
        node = backward_parent[meeting_node]
        while node is not None:
            backward_path.append(node)
            node = backward_parent[node]

        return forward_path + backward_path


def _plain_dijkstra_with_stats(graph, start, end, criterion="distance"):
    """Run Dijkstra and return its path, cost, and expansion statistics."""

    if not graph.has_station(start):
        raise ValueError(f"Station '{start}' does not exist.")
    if not graph.has_station(end):
        raise ValueError(f"Station '{end}' does not exist.")

    if start == end:
        return [start], 0, {"nodes_expanded": 0}

    dist = {start: 0}
    parent = {start: None}
    visited = set()
    pq = [(0, start)]
    nodes_expanded = 0

    while pq:
        current_cost, current = heapq.heappop(pq)

        if current in visited or current_cost != dist[current]:
            continue  # stale entry, skip (does not affect correctness)

        visited.add(current)
        nodes_expanded += 1

        if current == end:
            break

        for edge in graph.get_neighbors(current):
            neighbor = edge.destination
            weight = getattr(edge, criterion)

            if weight < 0:
                raise ValueError(
                    "Dijkstra requires non-negative edge weights; use "
                    "Bellman-Ford for graphs with negative weights (T2.4)."
                )

            if neighbor in visited:
                continue

            new_cost = current_cost + weight
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    if end not in dist:
        return None, None, {"nodes_expanded": nodes_expanded}

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, dist[end], {"nodes_expanded": nodes_expanded}


def compare_with_dijkstra(graph, start, end, criterion="distance"):
    """Compare Dijkstra and bidirectional Dijkstra on the same query."""

    plain_path, plain_cost, plain_stats = _plain_dijkstra_with_stats(
        graph, start, end, criterion
    )

    bidi = BidirectionalDijkstra(graph)
    bidi_path, bidi_cost, bidi_stats = bidi.find_shortest_path(start, end, criterion)

    plain_nodes = plain_stats["nodes_expanded"]
    bidi_nodes = bidi_stats["nodes_expanded"]
    reduction_pct = (
        round(100 * (plain_nodes - bidi_nodes) / plain_nodes, 1)
        if plain_nodes > 0
        else 0.0
    )

    return {
        "start": start,
        "end": end,
        "criterion": criterion,
        "dijkstra": {
            "path": plain_path,
            "cost": plain_cost,
            "nodes_expanded": plain_nodes,
        },
        "bidirectional_dijkstra": {
            "path": bidi_path,
            "cost": bidi_cost,
            "nodes_expanded": bidi_nodes,
        },
        "nodes_expanded_reduction_percent": reduction_pct,
    }
