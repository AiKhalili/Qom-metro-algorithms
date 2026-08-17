class Passenger:
    """Represents a passenger arriving at a gate."""

    def __init__(self, passenger_id, arrival_time):
        self.passenger_id = passenger_id
        self.arrival_time = arrival_time
        self.gate_id = None
        self.service_start = None
        self.service_end = None
        self.wait_time = None

    def __repr__(self):
        return (
            f"Passenger(id={self.passenger_id}, arrival={self.arrival_time:.2f}, "
            f"gate={self.gate_id}, wait={self.wait_time})"
        )
