class Edge:
    """
    Represents a connection between two stations.

    Stores the destination, distance, and travel time required by T1.1.
    Weight and capacity are included for reuse in later algorithms.
    """

    def __init__(self, destination, distance, time, weight=None, capacity=None):
        self.destination = destination
        self.distance = distance
        self.time = time
        self.weight = weight if weight is not None else distance
        self.capacity = capacity

    def __repr__(self):
        return (
            f"Edge(-> {self.destination}, distance={self.distance}, "
            f"time={self.time}, weight={self.weight})"
        )
