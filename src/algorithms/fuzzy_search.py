class FuzzyStationSearch:
    """T4.5: Find station names using Levenshtein edit distance."""

    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def _levenshtein_distance(a, b):
        """Return the Levenshtein edit distance between two strings."""
        if len(a) < len(b):
            a, b = b, a

        if not b:
            return len(a)

        previous = list(range(len(b) + 1))

        for i, char_a in enumerate(a, start=1):
            current = [i]

            for j, char_b in enumerate(b, start=1):
                cost = 0 if char_a == char_b else 1

                current.append(
                    min(
                        previous[j] + 1,
                        current[j - 1] + 1,
                        previous[j - 1] + cost,
                    )
                )

            previous = current

        return previous[-1]

    def search(self, query, top_n=1):
        """
        Return the closest station names and their edit distances.
        """
        if not isinstance(top_n, int) or top_n < 1:
            raise ValueError("top_n must be a positive integer.")

        stations = self.graph.get_stations()

        results = [
            (station, self._levenshtein_distance(query, station))
            for station in stations
        ]

        results.sort(key=lambda item: item[1])
        return results[:top_n]

    def closest_match(self, query):
        """Return the closest station name and its edit distance."""
        return self.search(query, top_n=1)[0]
