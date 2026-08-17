import heapq
import random

from data_structures.passenger import Passenger


class PassengerArrivalSimulation:
    """T3.4: Simulate random passenger arrivals and gate queues."""

    def __init__(self, num_gates, arrival_rate, service_time, random_seed=None):
        if num_gates < 1:
            raise ValueError("num_gates must be at least 1.")
        if arrival_rate <= 0:
            raise ValueError("arrival_rate must be positive.")

        self._num_gates = num_gates
        self._arrival_rate = arrival_rate
        self._service_time = service_time
        self._random = random.Random(random_seed)

    def _next_service_duration(self):
        if callable(self._service_time):
            return self._service_time()
        return self._service_time

    def _generate_arrival_times(self, num_passengers):
        """Generate random passenger arrival times."""
        arrival_times = []
        current_time = 0.0

        for _ in range(num_passengers):
            current_time += self._random.expovariate(self._arrival_rate)
            arrival_times.append(current_time)

        return arrival_times

    def run(self, num_passengers):
        """Simulate random passenger arrivals."""
        if num_passengers < 0:
            raise ValueError("num_passengers must be non-negative.")

        arrival_times = self._generate_arrival_times(num_passengers)
        return self.run_with_arrivals(arrival_times)

    def run_with_arrivals(self, arrival_times):
        """Run the simulation using given arrival times."""
        gate_heap = [(0.0, gate_id) for gate_id in range(self._num_gates)]
        heapq.heapify(gate_heap)

        passengers = []

        for i, arrival_time in enumerate(arrival_times):
            passenger = Passenger(passenger_id=i, arrival_time=arrival_time)

            gate_free_at, gate_id = heapq.heappop(gate_heap)

            service_start = max(arrival_time, gate_free_at)
            duration = self._next_service_duration()
            service_end = service_start + duration

            passenger.gate_id = gate_id
            passenger.service_start = service_start
            passenger.service_end = service_end
            passenger.wait_time = service_start - arrival_time

            heapq.heappush(gate_heap, (service_end, gate_id))
            passengers.append(passenger)

        return passengers

    @staticmethod
    def average_wait_time(passengers):
        """Return the average passenger waiting time."""
        if not passengers:
            return 0

        return sum(p.wait_time for p in passengers) / len(passengers)

    @staticmethod
    def max_wait_time(passengers):
        """Return the maximum passenger waiting time."""
        if not passengers:
            return 0

        return max(p.wait_time for p in passengers)

    @staticmethod
    def gate_utilization(passengers, num_gates, total_time=None):
        """Return the utilization of each gate."""
        if not passengers:
            return {gate_id: 0.0 for gate_id in range(num_gates)}

        if total_time is None:
            total_time = max(p.service_end for p in passengers)

        if total_time == 0:
            return {gate_id: 0.0 for gate_id in range(num_gates)}

        busy_time = {gate_id: 0.0 for gate_id in range(num_gates)}

        for passenger in passengers:
            busy_time[passenger.gate_id] += (
                passenger.service_end - passenger.service_start
            )

        return {
            gate_id: busy_time[gate_id] / total_time for gate_id in range(num_gates)
        }
