"""
runtime_controller.py

Main Runtime Controller.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\EnergyPlusV26-1-0")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pyenergyplus.api import EnergyPlusAPI
from memory.history_buffer import HistoryBuffer
from metrics.live_metrics_engine import LiveMetricsEngine
from handle_manager import HandleManager
from sensor_reader import SensorReader
from runtime_callbacks import RuntimeCallbacks
from agents.assessment_agent import AssessmentAgent

history_buffer = HistoryBuffer()
metrics_engine = LiveMetricsEngine()
assessment_agent = AssessmentAgent()

# ------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

config = json.load(

    open(

        PROJECT_ROOT / "config" / "runtime_config.json"

    )

)

# ------------------------------------------------------

api = EnergyPlusAPI()

state = api.state_manager.new_state()

# ------------------------------------------------------

handle_manager = HandleManager()

sensor_reader = SensorReader(

    api,

    handle_manager

)

callbacks = RuntimeCallbacks(
    api,
    handle_manager,
    sensor_reader,
    metrics_engine,
    assessment_agent,
    history_buffer
)

# ------------------------------------------------------

api.runtime.callback_after_predictor_before_hvac_managers(

    state,

    callbacks.after_predictor

)

# ------------------------------------------------------

arguments = [

    "-r",
    "-w",

    str(

        PROJECT_ROOT / config["weather"]

    ),

    "-d",

    str(

        PROJECT_ROOT /

        config["output_directory"]

    ),

    str(

        PROJECT_ROOT /

        config["idf"]

    )

]

print()

print("=" * 60)

print("Running EnergyPlus Runtime")

print("=" * 60)
print(arguments)

api.runtime.run_energyplus(

    state,

    arguments

)

print()

print("=" * 60)

print("Simulation Finished")

print("=" * 60)