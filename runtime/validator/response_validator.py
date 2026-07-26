from runtime.validator.validation_result import ValidationResult


class ResponseValidator:

    MIN_CONFIDENCE = 0.70

    COOLING_MIN = 22
    COOLING_MAX = 28

    HEATING_MIN = 18
    HEATING_MAX = 24

    MAX_DELTA = 3

    VALID_ACTUATORS = [

        "Cooling Setpoint",
        "Heating Setpoint",
        "Lighting Level",
        "Ventilation Rate"

    ]

    def validate(self, decision):

        errors = []

        # -----------------------

        if decision.confidence < self.MIN_CONFIDENCE:

            errors.append(
                "Confidence below threshold."
            )

        # -----------------------

        if len(decision.actions) == 0:

            errors.append(
                "No actions returned."
            )

        # -----------------------

        for action in decision.actions:

            if action.actuator not in self.VALID_ACTUATORS:

                errors.append(

                    f"Unknown actuator: {action.actuator}"

                )

                continue

            if action.actuator == "Cooling Setpoint":

                if not (

                    self.COOLING_MIN
                    <= action.target
                    <= self.COOLING_MAX

                ):

                    errors.append(

                        "Cooling setpoint out of range."

                    )

            if action.actuator == "Heating Setpoint":

                if not (

                    self.HEATING_MIN
                    <= action.target
                    <= self.HEATING_MAX

                ):

                    errors.append(

                        "Heating setpoint out of range."

                    )

            if abs(action.delta) > self.MAX_DELTA:

                errors.append(

                    "Temperature change exceeds safe limit."

                )

        # -----------------------

        if not (

            0 <= decision.estimated_energy_saving_percent <= 100

        ):

            errors.append(

                "Estimated energy saving invalid."

            )

        if not (

            0 <= decision.estimated_carbon_reduction_percent <= 100

        ):

            errors.append(

                "Estimated carbon reduction invalid."

            )

        return ValidationResult(

            valid=len(errors) == 0,

            errors=errors

        )