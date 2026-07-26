"""
decision_scheduler.py

Determines when the AI should make a decision.
"""


class DecisionScheduler:

    def __init__(

        self,

        interval=4

    ):

        self.interval = interval

        self.counter = 0

    # ----------------------------------------

    def should_run(self):

        self.counter += 1

        if self.counter >= self.interval:

            self.counter = 0

            return True

        return False