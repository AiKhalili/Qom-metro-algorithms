import heapq
import itertools

from data_structures.train import Train


class DispatchQueue:
    """T3.2: Priority queue for dispatching trains."""

    _REMOVED = "<removed-train>"

    def __init__(self):
        self._heap = []
        self._entry_finder = {}
        self._counter = itertools.count()

    def add_train(self, train):
        """Add a train to the queue."""
        if train.train_id in self._entry_finder:
            self.remove_train(train.train_id)

        count = next(self._counter)
        entry = [-train.priority, count, train]
        self._entry_finder[train.train_id] = entry
        heapq.heappush(self._heap, entry)

    def remove_train(self, train_id):
        """Remove a train by id."""
        entry = self._entry_finder.pop(train_id, None)

        if entry is None:
            return False

        entry[-1] = self._REMOVED
        return True

    def dispatch_next(self):
        """Remove and return the highest-priority train."""
        while self._heap:
            _, _, train = heapq.heappop(self._heap)

            if train is not self._REMOVED:
                del self._entry_finder[train.train_id]
                return train

        return None

    def peek_next(self):
        """Return the highest-priority train without removing it."""
        while self._heap and self._heap[0][-1] is self._REMOVED:
            heapq.heappop(self._heap)

        return self._heap[0][-1] if self._heap else None

    def update_priority(self, train_id, new_priority):
        """Update the priority of a train."""
        entry = self._entry_finder.get(train_id)

        if entry is None:
            raise KeyError(f"Train '{train_id}' is not in the dispatch queue.")

        train = entry[-1]
        train.priority = new_priority
        self.add_train(train)

    def is_empty(self):
        return len(self._entry_finder) == 0

    def size(self):
        return len(self._entry_finder)
