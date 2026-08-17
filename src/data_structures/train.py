class Train:
    """Represents a train and its platform time interval."""

    def __init__(self, train_id, arrival_time, departure_time, priority=0):
        if arrival_time >= departure_time:
            raise ValueError(
                f"Train '{train_id}': arrival_time must be before departure_time."
            )

        self.train_id = train_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.priority = priority

    def duration(self):
        """Return the platform occupation time."""
        return self.departure_time - self.arrival_time

    def overlaps(self, other):
        """Return True if this train overlaps another train."""
        return (
            self.arrival_time < other.departure_time
            and other.arrival_time < self.departure_time
        )

    def __repr__(self):
        return (
            f"Train({self.train_id}, arrival={self.arrival_time}, "
            f"departure={self.departure_time})"
        )

    def __eq__(self, other):
        if not isinstance(other, Train):
            return NotImplemented
        return self.train_id == other.train_id

    def __hash__(self):
        return hash(self.train_id)
