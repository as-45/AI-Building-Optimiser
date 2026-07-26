# It is just an in-memory queue and not chromaDB

"""
history_buffer.py

Stores recent BuildingState objects.
"""

from collections import deque


class HistoryBuffer:

    def __init__(self, max_history=4):
        """
        max_history = number of timesteps.

        4 timesteps
        =
        1 hour
        (15 min timestep)
        """

        self.buffer = deque(maxlen=max_history)

    # ----------------------------

    def add(self, building_state):

        self.buffer.append(building_state)

    # ----------------------------

    def latest(self):

        if len(self.buffer) == 0:
            return None

        return self.buffer[-1]

    # ----------------------------

    def previous(self):

        if len(self.buffer) < 2:
            return None

        return self.buffer[-2]

    # ----------------------------

    def history(self):

        return list(self.buffer)

    # ----------------------------

    def is_full(self):

        return len(self.buffer) == self.buffer.maxlen