from data.qom_metro_data import STATIONS, CONNECTIONS
from graph.graph import Graph


def build_incentive_network():
    """Build the Qom metro graph with negative incentive edges."""

    graph = Graph()

    for station in STATIONS:
        graph.add_station(station)

    for from_station, to_station, distance, time in CONNECTIONS:
        graph.add_connection(
            from_station,
            to_station,
            distance,
            time,
            weight=distance,
        )

    graph.add_connection(
        "ایستگاه میدان بقیه الله",
        "ایستگاه پردیسان",
        5,
        8,
        weight=-1.5,
        directed=True,
    )

    graph.add_connection(
        "ایستگاه پردیسان",
        "ایستگاه بوستان جنگلی غدیر",
        3.5,
        6,
        weight=-1,
        directed=True,
    )

    return graph


def build_incentive_network_with_negative_cycle():
    """Build a small graph containing a negative cycle."""

    graph = Graph()

    graph.add_connection(
        "A",
        "B",
        1,
        1,
        weight=4,
        directed=True,
    )

    graph.add_connection(
        "B",
        "C",
        1,
        1,
        weight=-6,
        directed=True,
    )

    graph.add_connection(
        "C",
        "A",
        1,
        1,
        weight=1,
        directed=True,
    )

    graph.add_connection(
        "A",
        "D",
        1,
        1,
        weight=10,
        directed=True,
    )

    return graph
