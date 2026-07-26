"""
comfort.py

Converts PMV into a human-readable comfort report.
"""

from metrics.pmv import PMVEngine


class ComfortEngine:

    def __init__(self):

        self.pmv = PMVEngine()

    # -----------------------------------------------------

    def evaluate(

        self,

        air_temperature,

        humidity

    ):

        result = self.pmv.evaluate(

            air_temperature,

            humidity

        )

        pmv = result["pmv"]

        ppd = result["ppd"]

        # ------------------------
        # Thermal Sensation
        # ------------------------

        if pmv <= -2.5:

            sensation = "Cold"

        elif pmv <= -1.5:

            sensation = "Cool"

        elif pmv <= -0.5:

            sensation = "Slightly Cool"

        elif pmv < 0.5:

            sensation = "Neutral"

        elif pmv < 1.5:

            sensation = "Slightly Warm"

        elif pmv < 2.5:

            sensation = "Warm"

        else:

            sensation = "Hot"

        # ------------------------
        # Comfort Level
        # ------------------------

        if abs(pmv) <= 0.5:

            level = "Excellent"

            score = 100 - ppd

        elif abs(pmv) <= 1:

            level = "Acceptable"

            score = 80 - ppd

        elif abs(pmv) <= 2:

            level = "Poor"

            score = 50 - ppd

        else:

            level = "Very Poor"

            score = 20 - ppd

        return {

    # Backward compatibility
    "metric": "comfort",

    "status": level,

    "reason": [

        f"PMV = {float(pmv)}",

        f"PPD = {float(ppd)}%",

        f"Thermal Sensation = {sensation}"

    ],

    # New PMV data
    "pmv": pmv,

    "ppd": ppd,

    "thermal_sensation": sensation,

    "comfort_level": level,

    "score": round(score, 2)

}