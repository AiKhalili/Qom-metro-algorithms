"""
T3.1 - Test scenario for PlatformScheduling (Interval Scheduling).

Scenario: several trains want to use the shared platform at
"ایستگاه راه آهن قم" during the same time window. We check that the
greedy algorithm selects the maximum number of non-overlapping trains.
"""

from algorithms.platform_scheduling import PlatformScheduling
from data_structures.train import Train


def build_sample_trains():
    """
    Timeline (minutes from start of shift):

    T1  [0, 4)
    T2  [1, 5)   -> overlaps T1
    T3  [4, 7)   -> touches T1, does not overlap
    T4  [5, 9)   -> overlaps T3, touches T2
    T5  [8, 10)  -> touches T4
    T6  [12, 15) -> disjoint from everything

    Optimal (max count) selection by earliest finish time:
    T1, T3, T5, T6  -> 4 trains
    """
    return [
        Train("T1", arrival_time=0, departure_time=4),
        Train("T2", arrival_time=1, departure_time=5),
        Train("T3", arrival_time=4, departure_time=7),
        Train("T4", arrival_time=5, departure_time=9),
        Train("T5", arrival_time=8, departure_time=10),
        Train("T6", arrival_time=12, departure_time=15),
    ]


def test_select_returns_optimal_count():
    scheduler = PlatformScheduling(build_sample_trains())

    selected, count = scheduler.select()

    assert count == 4
    assert [t.train_id for t in selected] == ["T1", "T3", "T5", "T6"]


def test_rejected_trains_are_the_complement_of_selected():
    scheduler = PlatformScheduling(build_sample_trains())

    selected, _ = scheduler.select()
    rejected = scheduler.rejected()

    selected_ids = {t.train_id for t in selected}
    rejected_ids = {t.train_id for t in rejected}

    assert selected_ids.isdisjoint(rejected_ids)
    assert selected_ids | rejected_ids == {"T1", "T2", "T3", "T4", "T5", "T6"}


def test_empty_input_returns_empty_selection():
    scheduler = PlatformScheduling([])

    selected, count = scheduler.select()

    assert selected == []
    assert count == 0


def test_single_train_is_always_selected():
    scheduler = PlatformScheduling([Train("SOLO", 0, 10)])

    selected, count = scheduler.select()

    assert count == 1
    assert selected[0].train_id == "SOLO"


if __name__ == "__main__":
    test_select_returns_optimal_count()
    test_rejected_trains_are_the_complement_of_selected()
    test_empty_input_returns_empty_selection()
    test_single_train_is_always_selected()
    print("T3.1 platform_scheduling: all scenarios passed.")
