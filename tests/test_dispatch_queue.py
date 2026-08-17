"""
T3.2 - Test scenario for DispatchQueue (priority queue for dispatch).

Scenario: trains arrive at the dispatch office with different delay
levels (higher priority = more urgent = dispatched first). We check
that dispatch_next always returns trains in decreasing priority order,
and that priority updates / removals are reflected correctly.
"""

from algorithms.dispatch_queue import DispatchQueue
from data_structures.train import Train


def test_dispatch_next_respects_priority_order():
    queue = DispatchQueue()

    # Simulate trains registering for dispatch with a delay-based priority
    queue.add_train(Train("A", 0, 5, priority=2))
    queue.add_train(Train("B", 0, 5, priority=5))  # most urgent (highest delay)
    queue.add_train(Train("C", 0, 5, priority=3))

    order = []
    while not queue.is_empty():
        train = queue.dispatch_next()
        order.append(train.train_id)

    assert order == ["B", "C", "A"]


def test_peek_next_does_not_remove():
    queue = DispatchQueue()
    queue.add_train(Train("A", 0, 5, priority=1))
    queue.add_train(Train("B", 0, 5, priority=9))

    top = queue.peek_next()
    assert top.train_id == "B"
    assert queue.size() == 2  # nothing removed


def test_update_priority_changes_dispatch_order():
    queue = DispatchQueue()
    queue.add_train(Train("A", 0, 5, priority=1))
    queue.add_train(Train("B", 0, 5, priority=2))

    # "A" suddenly becomes an emergency train
    queue.update_priority("A", new_priority=10)

    assert queue.dispatch_next().train_id == "A"
    assert queue.dispatch_next().train_id == "B"


def test_remove_train_excludes_it_from_dispatch():
    queue = DispatchQueue()
    queue.add_train(Train("A", 0, 5, priority=1))
    queue.add_train(Train("B", 0, 5, priority=2))

    removed = queue.remove_train("B")
    assert removed is True

    assert queue.dispatch_next().train_id == "A"
    assert queue.dispatch_next() is None


def test_dispatch_next_on_empty_queue_returns_none():
    queue = DispatchQueue()
    assert queue.dispatch_next() is None


if __name__ == "__main__":
    test_dispatch_next_respects_priority_order()
    test_peek_next_does_not_remove()
    test_update_priority_changes_dispatch_order()
    test_remove_train_excludes_it_from_dispatch()
    test_dispatch_next_on_empty_queue_returns_none()
    print("T3.2 dispatch_queue: all scenarios passed.")
