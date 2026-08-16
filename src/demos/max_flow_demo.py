"""
Demo for T4.2 - Maximum Flow using the shared project graph
extended with sample edge capacities.

"""

from algorithms.max_flow import MaxFlow
from data.qom_metro_data import CONNECTIONS, STATIONS
from data.qom_metro_capacity_data import CAPACITIES
from graph.graph import Graph


def build_capacity_graph():
    """Build the shared Qom metro graph, including passenger capacities."""
    graph = Graph()

    for station in STATIONS:
        graph.add_station(station)

    for origin, destination, distance, time in CONNECTIONS:
        graph.add_connection(origin, destination, distance, time)

    capacity_lookup = {
        (origin, destination): capacity for origin, destination, capacity in CAPACITIES
    }

    for station in graph.get_stations():
        for edge in graph.get_neighbors(station):
            key = (station, edge.destination)
            if key in capacity_lookup:
                edge.capacity = capacity_lookup[key]
            else:
                # reverse direction of an undirected connection
                reverse_key = (edge.destination, station)
                edge.capacity = capacity_lookup.get(reverse_key, 0)

    return graph


def demo_max_flow(graph):
    """T4.2: Compute peak-hour maximum passenger flow between two stations."""
    print("\n=== T4.2 - Maximum Flow (Peak-Hour Capacity) ===")

    source = "ایستگاه ترمینال مسافربری قم"
    sink = "ایستگاه حرم مطهر حضرت معصومه (س)"

    assert graph.has_station(source)
    assert graph.has_station(sink)

    max_flow = MaxFlow(graph)
    flow_value, flow_per_edge = max_flow.find_max_flow(source, sink)

    print(f"Source: {source}")
    print(f"Sink:   {sink}")
    print(f"Maximum passengers/minute deliverable: {flow_value}")
    print("Flow carried per edge:")
    for (u, v), amount in flow_per_edge.items():
        print(f"  {u} -> {v}: {amount}")


def run_max_flow_demo():
    """Run the T4.2 demo using the shared capacity-extended graph."""
    graph = build_capacity_graph()

    print(
        f"Loaded shared graph: "
        f"{graph.number_of_stations()} stations, "
        f"{graph.number_of_connections()} connections."
    )

    demo_max_flow(graph)


if __name__ == "__main__":
    run_max_flow_demo()
