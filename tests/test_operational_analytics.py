"""
T3.3 - Test scenario for OperationalAnalytics.

Scenario: trip records are logged over a few days for real Qom metro
stations. We check average daily trips and the k-th most visited
station queries.
"""

import pytest

from algorithms.operational_analytics import OperationalAnalytics
from data_structures.trip_record import TripRecord

HARAM = "ایستگاه حرم مطهر حضرت معصومه (س)"
TERMINAL = "ایستگاه ترمینال مسافربری قم"
DANESHGAH = "ایستگاه دانشگاه قم"


def build_sample_analytics():
    analytics = OperationalAnalytics()

    trips = [
        # Day 1: 3 trips at Haram, 1 at Terminal
        TripRecord(HARAM, "2026-05-01"),
        TripRecord(HARAM, "2026-05-01"),
        TripRecord(HARAM, "2026-05-01"),
        TripRecord(TERMINAL, "2026-05-01"),
        # Day 2: 2 trips at Haram, 2 at Terminal, 1 at Daneshgah
        TripRecord(HARAM, "2026-05-02"),
        TripRecord(HARAM, "2026-05-02"),
        TripRecord(TERMINAL, "2026-05-02"),
        TripRecord(TERMINAL, "2026-05-02"),
        TripRecord(DANESHGAH, "2026-05-02"),
    ]

    for trip in trips:
        analytics.record_trip(trip)

    return analytics


def test_total_and_average_daily_trips():
    analytics = build_sample_analytics()

    assert analytics.total_trips() == 9
    assert analytics.distinct_days() == 2
    assert analytics.average_daily_trips() == pytest.approx(4.5)


def test_visits_count_per_station():
    analytics = build_sample_analytics()

    assert analytics.visits(HARAM) == 5
    assert analytics.visits(TERMINAL) == 3
    assert analytics.visits(DANESHGAH) == 1
    assert analytics.visits("ایستگاه ناموجود") == 0


def test_kth_most_visited_station():
    analytics = build_sample_analytics()

    first = analytics.kth_most_visited_station(1)
    second = analytics.kth_most_visited_station(2)
    third = analytics.kth_most_visited_station(3)

    assert first == (HARAM, 5)
    assert second == (TERMINAL, 3)
    assert third == (DANESHGAH, 1)


def test_kth_out_of_range_raises():
    analytics = build_sample_analytics()

    with pytest.raises(ValueError):
        analytics.kth_most_visited_station(10)


def test_busiest_stations_top_k():
    analytics = build_sample_analytics()

    top2 = analytics.busiest_stations(2)

    assert top2 == [(HARAM, 5), (TERMINAL, 3)]


def test_empty_analytics_average_is_zero():
    analytics = OperationalAnalytics()
    assert analytics.average_daily_trips() == 0
    assert analytics.total_trips() == 0


if __name__ == "__main__":
    test_total_and_average_daily_trips()
    test_visits_count_per_station()
    test_kth_most_visited_station()
    test_kth_out_of_range_raises()
    test_busiest_stations_top_k()
    test_empty_analytics_average_is_zero()
    print("T3.3 operational_analytics: all scenarios passed.")
