"""
T3.4 - Test scenario for PassengerArrivalSimulation.

Scenario: passengers arrive randomly at the gates of a busy station
(e.g. "ایستگاه حرم مطهر حضرت معصومه (س)"). We check basic invariants:
wait times are non-negative, every passenger is assigned to a valid
gate, and a fixed random seed makes results reproducible.
"""

from algorithms.passenger_simulation import PassengerArrivalSimulation


def test_reproducible_with_fixed_seed():
    sim1 = PassengerArrivalSimulation(
        num_gates=2, arrival_rate=1.0, service_time=1.5, random_seed=42
    )
    sim2 = PassengerArrivalSimulation(
        num_gates=2, arrival_rate=1.0, service_time=1.5, random_seed=42
    )

    passengers1 = sim1.run(num_passengers=20)
    passengers2 = sim2.run(num_passengers=20)

    waits1 = [p.wait_time for p in passengers1]
    waits2 = [p.wait_time for p in passengers2]

    assert waits1 == waits2


def test_all_passengers_are_assigned_a_valid_gate():
    sim = PassengerArrivalSimulation(
        num_gates=3, arrival_rate=2.0, service_time=1.0, random_seed=1
    )

    passengers = sim.run(num_passengers=50)

    assert len(passengers) == 50
    for passenger in passengers:
        assert passenger.gate_id in {0, 1, 2}
        assert passenger.wait_time >= 0
        assert passenger.service_end >= passenger.service_start


def test_more_gates_reduce_or_equal_average_wait():
    common_kwargs = dict(arrival_rate=3.0, service_time=1.0, random_seed=7)

    sim_one_gate = PassengerArrivalSimulation(num_gates=1, **common_kwargs)
    sim_many_gates = PassengerArrivalSimulation(num_gates=5, **common_kwargs)

    # Same arrival stream for a fair comparison
    arrivals = sim_one_gate._generate_arrival_times(100)

    passengers_one = sim_one_gate.run_with_arrivals(arrivals)
    passengers_many = sim_many_gates.run_with_arrivals(arrivals)

    avg_wait_one = PassengerArrivalSimulation.average_wait_time(passengers_one)
    avg_wait_many = PassengerArrivalSimulation.average_wait_time(passengers_many)

    assert avg_wait_many <= avg_wait_one


def test_gate_utilization_returns_value_per_gate():
    sim = PassengerArrivalSimulation(
        num_gates=2, arrival_rate=2.0, service_time=1.0, random_seed=3
    )
    passengers = sim.run(num_passengers=30)

    utilization = PassengerArrivalSimulation.gate_utilization(passengers, num_gates=2)

    assert set(utilization.keys()) == {0, 1}
    for value in utilization.values():
        assert 0.0 <= value <= 1.0


def test_zero_passengers_returns_empty_list():
    sim = PassengerArrivalSimulation(
        num_gates=1, arrival_rate=1.0, service_time=1.0, random_seed=0
    )
    passengers = sim.run(num_passengers=0)

    assert passengers == []
    assert PassengerArrivalSimulation.average_wait_time(passengers) == 0
    assert PassengerArrivalSimulation.max_wait_time(passengers) == 0


if __name__ == "__main__":
    test_reproducible_with_fixed_seed()
    test_all_passengers_are_assigned_a_valid_gate()
    test_more_gates_reduce_or_equal_average_wait()
    test_gate_utilization_returns_value_per_gate()
    test_zero_passengers_returns_empty_list()
    print("T3.4 passenger_simulation: all scenarios passed.")
