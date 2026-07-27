"""EnergyPlus callback that collects feedback and applies safe controls."""

from scheduler.decision_scheduler import DecisionScheduler
from shared.runtime_state import RuntimeState


class RuntimeCallbacks:
    def __init__(
        self,
        api,
        handle_manager,
        sensor_reader,
        metrics_engine,
        assessment_agent,
        history_buffer,
        executor,
        config,
        runtime_loop=None,
    ):
        self.api = api
        self.handle_manager = handle_manager
        self.sensor_reader = sensor_reader
        self.metrics_engine = metrics_engine
        self.assessment_agent = assessment_agent
        self.history_buffer = history_buffer
        self.executor = executor
        self.config = config
        self.runtime_loop = runtime_loop
        self.initialized = False
        self.callback_counter = 0
        self.smoke_test_applications = 0
        self.decision_scheduler = DecisionScheduler(
            interval=config["decision_interval_callbacks"]
        )

    def after_predictor(self, state):
        """Runs every EnergyPlus timestep at the selected safe callback point."""
        self.callback_counter += 1

        if not self.initialized:
            if not self.api.exchange.api_data_fully_ready(state):
                return
            self.handle_manager.initialize(self.api, state)
            self.initialized = True

        building_state = self.sensor_reader.read(state)
        RuntimeState.building_state = building_state
        self.history_buffer.add(building_state)

        metrics_report = self.metrics_engine.evaluate(building_state)
        RuntimeState.metrics = metrics_report
        assessment = self.assessment_agent.assess(building_state, metrics_report)
        RuntimeState.assessment = assessment

        self._run_smoke_test()
        self._run_llm_step(building_state)

        self._log_status(building_state, assessment)

    def _run_smoke_test(self):
        """One deterministic action used to prove Python -> EnergyPlus control."""
        smoke_test = self.config["smoke_test"]
        if not smoke_test["enabled"]:
            return
        if self.smoke_test_applications >= smoke_test["apply_for_callbacks"]:
            return
        if self.api.exchange.warmup_flag(self.executor.state):
            return
        environment_number = self.api.exchange.current_environment_num(
            self.executor.state
        )
        if environment_number < smoke_test["minimum_environment_number"]:
            return

        self.executor.apply_action(
            actuator_name=smoke_test["actuator"],
            target=smoke_test["target"],
            source=f"deterministic_smoke_test_environment_{environment_number}",
            callback_number=self.callback_counter,
        )
        self.smoke_test_applications += 1

    def _run_llm_step(self, building_state):
        """LLM control remains off until the deterministic smoke test passes."""
        if not self.config["enable_llm_control"] or self.runtime_loop is None:
            return
        if not self.decision_scheduler.should_run():
            return

        try:
            result = self.runtime_loop.run_step(
                building_state=building_state,
                history=self.history_buffer.history(),
                current_episode=self.callback_counter,
                trigger={"trigger": "scheduled", "priority": "normal"},
                callback_number=self.callback_counter,
            )
            print("\n===== LLM Decision =====")
            print(result["decision"])
            print("\n===== Execution =====")
            print(result["execution"])
        except Exception as error:
            # Keep the EnergyPlus run alive; no action is applied after an error.
            print(f"LLM control step skipped safely: {error}")

    def _log_status(self, building_state, assessment):
        """Emit bounded ASCII-only progress output for Windows consoles."""
        interval = self.config["log_interval_callbacks"]
        if self.callback_counter % interval != 0:
            return
        print(
            "Runtime status | "
            f"callback={self.callback_counter} | "
            f"building_power_w={building_state.building_power:.1f} | "
            f"hvac_power_w={building_state.hvac_power:.1f} | "
            f"average_comfort={assessment['average_comfort']:.1f} | "
            f"uncomfortable_zones={assessment['uncomfortable_zones']}"
        )
