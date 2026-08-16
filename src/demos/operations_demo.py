"""
src/demos/operations_demo.py

Demo for T3.1-T3.4 using the shared project data and graph.

Run:
    python -m src.demos.operations_demo
"""

from algorithms.dispatch_queue import DispatchQueue
from algorithms.operational_analytics import OperationalAnalytics
from algorithms.passenger_simulation import PassengerArrivalSimulation
from algorithms.platform_scheduling import PlatformScheduling
from data.qom_metro_data import CONNECTIONS, STATIONS
from data_structures.train import Train
from data_structures.trip_record import TripRecord
from graph.graph import Graph


def build_graph():
    """Build the shared Qom metro graph."""
    graph = Graph()

    for station in STATIONS:
        graph.add_station(station)

    for origin, destination, distance, time in CONNECTIONS:
        graph.add_connection(origin, destination, distance, time)

    return graph


def demo_platform_scheduling(graph):
    """T3.1: Select non-overlapping trains for a shared platform."""
    print("\n=== T3.1 - Platform Scheduling (ایستگاه راه آهن قم) ===")

    assert graph.has_station("ایستگاه راه آهن قم")

    trains = [
        Train("QOM-101", arrival_time=0, departure_time=6),
        Train("QOM-102", arrival_time=2, departure_time=8),
        Train("QOM-103", arrival_time=6, departure_time=12),
        Train("QOM-104", arrival_time=9, departure_time=15),
        Train("QOM-105", arrival_time=12, departure_time=18),
    ]

    scheduler = PlatformScheduling(trains)
    selected, count = scheduler.select()
    rejected = scheduler.rejected()

    print(f"Trains requesting the platform: {[t.train_id for t in trains]}")
    print(f"Selected ({count}): {[t.train_id for t in selected]}")
    print(f"Rejected: {[t.train_id for t in rejected]}")

    return selected


def demo_dispatch_queue(scheduled_trains):
    """T3.2: Dispatch scheduled trains by delay priority."""
    print("\n=== T3.2 - Dispatch Queue ===")

    delay_minutes = {
        "QOM-101": 2,
        "QOM-103": 9,
        "QOM-105": 4,
    }

    queue = DispatchQueue()

    for train in scheduled_trains:
        train.priority = delay_minutes.get(train.train_id, 0)
        queue.add_train(train)

    print(f"Queue size before dispatch: {queue.size()}")

    dispatch_order = []

    while not queue.is_empty():
        train = queue.dispatch_next()
        dispatch_order.append(train.train_id)

    print(f"Dispatch order (most delayed first): {dispatch_order}")


def demo_operational_analytics(graph):
    """T3.3: Analyze trip records from real stations."""
    print("\n=== T3.3 - Operational Analytics ===")

    haram = "ایستگاه حرم مطهر حضرت معصومه (س)"
    terminal = "ایستگاه ترمینال مسافربری قم"
    daneshgah = "ایستگاه دانشگاه قم"

    for station in (haram, terminal, daneshgah):
        assert graph.has_station(station)

    analytics = OperationalAnalytics()

    sample_trips = (
        [TripRecord(haram, "2026-05-01")] * 30
        + [TripRecord(terminal, "2026-05-01")] * 12
        + [TripRecord(haram, "2026-05-02")] * 25
        + [TripRecord(terminal, "2026-05-02")] * 18
        + [TripRecord(daneshgah, "2026-05-02")] * 7
    )

    for trip in sample_trips:
        analytics.record_trip(trip)

    print(f"Total trips: {analytics.total_trips()}")
    print(f"Average daily trips: {analytics.average_daily_trips():.1f}")
    print(f"Busiest station (k=1): {analytics.kth_most_visited_station(1)}")
    print(f"Top 3 busiest stations: {analytics.busiest_stations(3)}")


def demo_passenger_simulation(graph):
    """T3.4: Simulate passenger arrivals at a real station."""
    print("\n=== T3.4 - Passenger Arrival Simulation ===")

    station = "ایستگاه حرم مطهر حضرت معصومه (س)"
    assert graph.has_station(station)

    print(f"Simulating passenger arrivals at: {station}")

    simulation = PassengerArrivalSimulation(
        num_gates=3,
        arrival_rate=2.0,
        service_time=1.2,
        random_seed=42,
    )

    passengers = simulation.run(num_passengers=200)

    avg_wait = PassengerArrivalSimulation.average_wait_time(passengers)
    max_wait = PassengerArrivalSimulation.max_wait_time(passengers)
    utilization = PassengerArrivalSimulation.gate_utilization(
        passengers,
        num_gates=3,
    )

    print(f"Passengers simulated: {len(passengers)}")
    print(f"Average wait time: {avg_wait:.2f} minutes")
    print(f"Max wait time: {max_wait:.2f} minutes")
    print(f"Gate utilization: {utilization}")


def run_operations_demo():
    """Run all T3 operations using the shared graph."""
    graph = build_graph()

    print(
        f"Loaded shared graph: "
        f"{graph.number_of_stations()} stations, "
        f"{graph.number_of_connections()} connections."
    )

    selected_trains = demo_platform_scheduling(graph)
    demo_dispatch_queue(selected_trains)
    demo_operational_analytics(graph)
    demo_passenger_simulation(graph)


if __name__ == "__main__":
    run_operations_demo()
