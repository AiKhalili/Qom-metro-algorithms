from .edge import Edge


class Graph:
    """
    Represents the Qom metro network using an adjacency list.

    Each station is a vertex and each connection is an edge.
    Each edge stores distance and travel time as required by T1.1.
    The graph also supports directed edges for later tasks.
    """

    def __init__(self):
        self._adjacency_list = {}
        self._connection_count = 0

    # station management

    def add_station(self, station):
        """Add a station if it does not already exist."""
        if station not in self._adjacency_list:
            self._adjacency_list[station] = []

    def has_station(self, station):
        """Return True if the station exists."""
        return station in self._adjacency_list

    def get_stations(self):
        """Return all stations in the graph."""
        return list(self._adjacency_list.keys())

    def number_of_stations(self):
        """Return the total number of stations."""
        return len(self._adjacency_list)

    # connection management

    def add_connection(
        self,
        station1,
        station2,
        distance,
        time,
        weight=None,
        directed=False,
        capacity=None,
    ):
        """
        Add a connection between two stations.

        Undirected connections are stored in both directions.
        Weight and capacity are available for later tasks.
        """
        self.add_station(station1)
        self.add_station(station2)

        self._adjacency_list[station1].append(
            Edge(station2, distance, time, weight, capacity)
        )

        if not directed:
            self._adjacency_list[station2].append(
                Edge(station1, distance, time, weight, capacity)
            )

        self._connection_count += 1

    def get_neighbors(self, station):
        """Return the outgoing edges of a station."""
        if station not in self._adjacency_list:
            raise ValueError(f"Station '{station}' does not exist.")
        return self._adjacency_list[station]

    def number_of_connections(self):
        """Return the number of logical connections."""
        return self._connection_count

    # utility

    def display(self):
        """Print the whole graph in a readable form."""
        for station, edges in self._adjacency_list.items():
            print(f"{station}:")
            for edge in edges:
                print(f"  {edge}")
