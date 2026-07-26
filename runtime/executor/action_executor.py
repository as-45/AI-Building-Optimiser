from runtime.executor.execution_result import ExecutionResult


class ActionExecutor:

    def execute(self, decision):

        applied = []

        errors = []

        for action in decision.actions:

            applied.append(

                f"{action.actuator} -> {action.target}"

            )

        return ExecutionResult(

            success=True,

            applied_actions=applied,

            errors=errors

        )