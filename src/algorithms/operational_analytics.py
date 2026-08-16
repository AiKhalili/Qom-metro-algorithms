from collections import Counter

from src.data_structures.trip_record import TripRecord


class OperationalAnalytics:
    """T3.3: Analyze operational data from passenger trips."""

    def __init__(self):
        self._station_counts = Counter()
        self._date_counts = Counter()
        self._total_trips = 0

    def record_trip(self, trip):
        """Register a passenger trip."""
        self._station_counts[trip.station] += 1
        self._date_counts[trip.trip_date] += 1
        self._total_trips += 1

    def total_trips(self):
        """Return the total number of recorded trips."""
        return self._total_trips

    def distinct_days(self):
        """Return the number of days with recorded trips."""
        return len(self._date_counts)

    def average_daily_trips(self):
        """Return the average number of trips per recorded day."""
        if not self._date_counts:
            return 0
        return self._total_trips / len(self._date_counts)

    def visits(self, station):
        """Return the number of trips recorded at a station."""
        return self._station_counts.get(station, 0)

    def _ranked_stations(self):
        """Return stations sorted by trip count."""
        return sorted(
            self._station_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )

    def kth_most_visited_station(self, k):
        """Return the k-th most visited station and its trip count."""
        ranked = self._ranked_stations()

        if k < 1 or k > len(ranked):
            raise ValueError(
                f"k={k} is out of range; there are {len(ranked)} distinct "
                "stations with recorded trips."
            )

        return ranked[k - 1]

    def busiest_stations(self, k):
        """Return the top-k most visited stations."""
        if k < 0:
            raise ValueError("k must be non-negative.")

        return self._ranked_stations()[:k]
