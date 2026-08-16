"""
Demo for T4.3 - Articulation Points & Bridges using the shared project graph.

"""

from algorithms.critical_stations import CriticalStations
from data.qom_metro_data import CONNECTIONS, STATIONS
from graph.graph import Graph


def build_graph():
    """Build the shared Qom metro graph."""
    graph = Graph()

    for station in STATIONS:
        graph.add_station(station)

    for origin, destination, distance, time in CONNECTIONS:
        graph.add_connection(origin, destination, distance, time)

    return graph


def demo_critical_stations(graph):
    """T4.3: Identify articulation points and bridges in the network."""
    print("\n=== T4.3 - Critical Stations (Articulation Points & Bridges) ===")

    analyzer = CriticalStations(graph)
    analyzer.analyze()

    articulation_points = analyzer.get_articulation_points()
    bridges = analyzer.get_bridges()

    print(f"Articulation points ({len(articulation_points)}):")
    for station in articulation_points:
        print(f"  - {station}")

    print(f"\nBridges ({len(bridges)}):")
    for u, v in bridges:
        print(f"  - {u}  <->  {v}")


def run_critical_stations_demo():
    """Run the T4.3 demo using the shared graph."""
    graph = build_graph()

    print(
        f"Loaded shared graph: "
        f"{graph.number_of_stations()} stations, "
        f"{graph.number_of_connections()} connections."
    )

    demo_critical_stations(graph)


if __name__ == "__main__":
    run_critical_stations_demo()
