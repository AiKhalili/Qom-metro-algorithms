"""
Demo for T4.4 - Relief Team Deployment
using the shared metro graph.
"""

from algorithms.relief_deployment import ReliefDeployment
from data.qom_metro_data import CONNECTIONS, STATIONS
from graph.graph import Graph


def build_graph():
    """Build shared Qom metro graph."""

    graph = Graph()

    for station in STATIONS:
        graph.add_station(station)

    for origin, destination, distance, time in CONNECTIONS:
        graph.add_connection(origin, destination, distance, time)

    return graph


def demo_relief_deployment(graph):

    print("\n=== T4.4 - Relief Team Deployment ===")

    deployment = ReliefDeployment(graph)

    greedy_result = deployment.greedy_dominating_set()

    print(f"Greedy solution size: {len(greedy_result)}")

    print("Relief centers:")

    for station in sorted(greedy_result):
        print(f"  - {station}")

    # Test scenario: verify coverage
    assert deployment.is_dominating_set(greedy_result)

    print("Verified: all stations are covered.")

    exact_result = deployment.exact_minimum_dominating_set()

    print(f"\nOptimal solution size: {len(exact_result)}")

    ratio = deployment.approximation_ratio(greedy_result, exact_result)

    print(f"Approximation ratio: {ratio:.2f}")


def run_relief_deployment_demo():

    graph = build_graph()

    print(
        f"Loaded shared graph: "
        f"{graph.number_of_stations()} stations, "
        f"{graph.number_of_connections()} connections."
    )

    demo_relief_deployment(graph)


if __name__ == "__main__":
    run_relief_deployment_demo()
