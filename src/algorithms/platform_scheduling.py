class PlatformScheduling:
    """
    T3.1: Select the maximum number of non-overlapping trains
    for a shared platform using Interval Scheduling.
    """

    def __init__(self, trains):
        self._trains = list(trains)

    def select(self):
        """
        Return (selected_trains, count) using earliest departure time.
        """
        if not self._trains:
            return [], 0

        sorted_trains = sorted(self._trains, key=lambda train: train.departure_time)

        selected = [sorted_trains[0]]
        last_departure = sorted_trains[0].departure_time

        for train in sorted_trains[1:]:
            if train.arrival_time >= last_departure:
                selected.append(train)
                last_departure = train.departure_time

        return selected, len(selected)

    def rejected(self):
        """Return trains that were not selected."""
        selected, _ = self.select()
        selected_ids = {train.train_id for train in selected}

        return [train for train in self._trains if train.train_id not in selected_ids]
