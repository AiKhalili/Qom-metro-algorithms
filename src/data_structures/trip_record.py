class TripRecord:
    """Represents a single passenger trip at a station."""

    def __init__(self, station, trip_date):
        self.station = station
        self.trip_date = trip_date

    def __repr__(self):
        return f"TripRecord(station={self.station!r}, date={self.trip_date!r})"
