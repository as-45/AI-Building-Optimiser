"""Applies validated decisions to the active EnergyPlus simulation."""

import csv
from datetime import datetime, timezone
from pathlib import Path

from runtime.executor.execution_result import ExecutionResult


class ActionExecutor:
    """Single safety boundary between a decision and an EnergyPlus actuator."""

    def __init__(self, api, state, handle_manager, action_log_path):
        self.api = api
        self.state = state
        self.handle_manager = handle_manager
        self.action_log_path = Path(action_log_path)
        self.action_log_path.parent.mkdir(parents=True, exist_ok=True)

    def apply_action(self, actuator_name, target, source, callback_number):
        """Apply one configured actuator value after range validation."""
        actuator = self.handle_manager.get_actuator(actuator_name)
        target = float(target)

        minimum = actuator["minimum"]
        maximum = actuator["maximum"]
        if not minimum <= target <= maximum:
            raise ValueError(
                f"Unsafe {actuator_name} target {target:.2f}; allowed range is "
                f"{minimum:.2f} to {maximum:.2f}."
            )

        self.api.exchange.set_actuator_value(
            self.state, actuator["handle"], target
        )
        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "callback": callback_number,
            "source": source,
            "actuator": actuator_name,
            "target": target,
            "status": "applied",
        }
        self._write_log(record)
        print(
            f"Applied EnergyPlus actuator: {actuator_name} = {target:.2f} "
            f"(source: {source})"
        )
        return record

    def execute(self, decision, callback_number=0):
        """Apply all actions from a validated Decision object."""
        applied, errors = [], []
        for action in decision.actions:
            try:
                record = self.apply_action(
                    action.actuator, action.target, "llm", callback_number
                )
                applied.append(f"{record['actuator']} -> {record['target']}")
            except (KeyError, ValueError) as error:
                errors.append(str(error))

        return ExecutionResult(
            success=not errors,
            applied_actions=applied,
            errors=errors,
        )

    def _write_log(self, record):
        write_header = not self.action_log_path.exists()
        with self.action_log_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(record)
