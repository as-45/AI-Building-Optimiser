"""
pmv.py

Calculates PMV and PPD using ASHRAE 55.
"""

import json
from pathlib import Path

from pythermalcomfort.models import pmv_ppd_ashrae


class PMVEngine:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        config_file = project_root / "config" / "comfort_config.json"

        with open(config_file, "r") as f:
            self.config = json.load(f)

    # -------------------------------------------------

    def evaluate(

        self,

        air_temperature,

        relative_humidity,

        mean_radiant_temperature=None

    ):

        if mean_radiant_temperature is None:

            if self.config["calculate_mrt_from_air"]:

                mean_radiant_temperature = air_temperature

            else:

                raise ValueError(

                    "Mean Radiant Temperature missing."

                )

        result = pmv_ppd_ashrae(

            tdb=air_temperature,

            tr=mean_radiant_temperature,

            vr=self.config["air_speed"],

            rh=relative_humidity,

            met=self.config["metabolic_rate"],

            clo=self.config["clothing_insulation"],

            limit_inputs=False

        )

        return {

            "pmv": round(result.pmv, 2),

            "ppd": round(result.ppd, 2)

        }