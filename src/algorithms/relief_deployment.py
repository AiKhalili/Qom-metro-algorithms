import itertools


class ReliefDeployment:
    """
    T4.4: Approximate Minimum Dominating Set for relief team deployment.
    Uses greedy approximation and exact search for comparison.
    """

    def __init__(self, graph):
        self.graph = graph

    def greedy_dominating_set(self):
        """
        Greedy approximation:
        Selects the station that covers the most uncovered stations.
        """
        stations = self.graph.get_stations()

        closed_neighborhood = {
            station: self._closed_neighborhood(station) for station in stations
        }

        uncovered = set(stations)
        dominating_set = set()

        while uncovered:
            best_station = max(
                stations,
                key=lambda s: len(closed_neighborhood[s] & uncovered),
            )

            newly_covered = closed_neighborhood[best_station] & uncovered

            if not newly_covered:
                dominating_set.update(uncovered)
                break

            dominating_set.add(best_station)
            uncovered -= newly_covered

        return dominating_set

    def _closed_neighborhood(self, station):
        """Return station and its direct neighbors."""
        neighbors = {edge.destination for edge in self.graph.get_neighbors(station)}

        neighbors.add(station)
        return neighbors

    def exact_minimum_dominating_set(self, max_stations=25):
        """
        Brute-force exact solution for small graphs.
        Used only for approximation comparison.
        """

        stations = self.graph.get_stations()

        if len(stations) > max_stations:
            raise ValueError(
                f"Graph has {len(stations)} stations; "
                f"exact search is limited to {max_stations}."
            )

        closed_neighborhood = {
            station: self._closed_neighborhood(station) for station in stations
        }

        all_stations = set(stations)

        for size in range(1, len(stations) + 1):

            for candidate in itertools.combinations(stations, size):

                covered = set()

                for station in candidate:
                    covered |= closed_neighborhood[station]

                if covered == all_stations:
                    return set(candidate)

        return all_stations

    def is_dominating_set(self, candidate_set):
        """Check whether every station is covered."""

        stations = set(self.graph.get_stations())

        for station in candidate_set:
            if not self.graph.has_station(station):
                raise ValueError(f"Station '{station}' does not exist.")

        covered = set()

        for station in candidate_set:
            covered |= self._closed_neighborhood(station)

        return covered >= stations

    def approximation_ratio(self, greedy_result, exact_result):
        """Return greedy size divided by optimal size."""

        if not exact_result:
            raise ValueError("exact_result must be non-empty.")

        return len(greedy_result) / len(exact_result)
