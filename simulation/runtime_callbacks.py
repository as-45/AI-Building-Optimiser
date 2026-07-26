"""
runtime_callbacks.py

EnergyPlus runtime callbacks.

Contains NO initialization logic.
"""

class RuntimeCallbacks:

    def __init__(

        self,

        api,

        handle_manager,

        sensor_reader,
        metrics_engine,
        assessment_agent,
        history_buffer

    ):

        self.api = api

        self.handle_manager = handle_manager

        self.sensor_reader = sensor_reader
        self.metrics_engine = metrics_engine
        self.assessment_agent = assessment_agent
        self.history_buffer = history_buffer

        self.initialized = False

        self.callback_counter = 0

    # --------------------------------------------------

    def after_predictor(self, state):

        """
        Called every timestep.

        """

        self.callback_counter += 1

        if not self.initialized:

            print("\nInitializing Handles...")

            self.handle_manager.initialize(

                self.api,

                state

            )

            self.initialized = True

            print("Initialization Complete\n")

        building_state = self.sensor_reader.read(state)
        self.history_buffer.add(building_state)
        previous = self.history_buffer.previous()
        if previous is not None:
            print("\n========== Temperature Trend ==========\n")
            for zone_name, current_zone in building_state.zones.items():
                previous_zone = previous.zones[zone_name]
                delta = current_zone.temperature - previous_zone.temperature
                trend = "Stable"
                if delta > 0.10:
                    trend = "Heating ↑"
                elif delta < -0.10:
                    trend = "Cooling ↓"

                print(f"{zone_name:25s}"f"{delta:+6.2f} °C   "f"{trend}")

            print()

        metrics_report = self.metrics_engine.evaluate(building_state)
        assessment = self.assessment_agent.assess(building_state,metrics_report)

        print(

            f"\nCallback {self.callback_counter}"

        )

        print(building_state)
        print("\n===== Metrics =====")
        print(metrics_report)
        print("\n===== Assessment =====")
        print(assessment)