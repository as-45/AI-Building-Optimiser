"""Entry point for the safe EnergyPlus runtime-control smoke test."""

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\EnergyPlusV26-1-0")
sys.path.insert(0, str(PROJECT_ROOT))

from pyenergyplus.api import EnergyPlusAPI

from agents.assessment_agent import AssessmentAgent
from metrics.live_metrics_engine import LiveMetricsEngine
from memory.history_buffer import HistoryBuffer
from runtime.executor.action_executor import ActionExecutor
from simulation.handle_manager import HandleManager
from simulation.runtime_callbacks import RuntimeCallbacks
from simulation.sensor_reader import SensorReader


def build_runtime_loop(config, executor):
    """Construct cloud-only dependencies only when LLM control is explicitly on."""
    if not config["enable_llm_control"]:
        return None

    from context.trend_analyzer import TrendAnalyzer
    from memory.memory_retriever import MemoryRetriever
    from runtime.mcp_client import MCPClient
    from runtime.runtime_loop import RuntimeLoop

    mcp_server = os.getenv("MCP_SERVER_URL")
    if not mcp_server:
        raise RuntimeError("Set MCP_SERVER_URL before enabling LLM control.")

    return RuntimeLoop(
        TrendAnalyzer(),
        MemoryRetriever() if config["enable_memory_retrieval"] else None,
        MCPClient(mcp_server),
        executor,
    )


def main():
    with (PROJECT_ROOT / "config" / "runtime_config.json").open(encoding="utf-8") as file:
        config = json.load(file)

    api = EnergyPlusAPI()
    state = api.state_manager.new_state()
    handle_manager = HandleManager()
    executor = ActionExecutor(
        api,
        state,
        handle_manager,
        PROJECT_ROOT / config["action_log"],
    )
    runtime_loop = build_runtime_loop(config, executor)
    callbacks = RuntimeCallbacks(
        api=api,
        handle_manager=handle_manager,
        sensor_reader=SensorReader(api, handle_manager),
        metrics_engine=LiveMetricsEngine(),
        assessment_agent=AssessmentAgent(),
        history_buffer=HistoryBuffer(),
        executor=executor,
        config=config,
        runtime_loop=runtime_loop,
    )

    api.runtime.callback_after_predictor_before_hvac_managers(
        state, callbacks.after_predictor
    )

    output_directory = PROJECT_ROOT / config["output_directory"]
    output_directory.mkdir(parents=True, exist_ok=True)
    arguments = [
        "-r",
        "-w",
        str(PROJECT_ROOT / config["weather"]),
        "-d",
        str(output_directory),
        str(PROJECT_ROOT / config["idf"]),
    ]
    print("\n" + "=" * 60)
    print("Running EnergyPlus runtime-control smoke test")
    print("=" * 60)
    print(arguments)
    status = api.runtime.run_energyplus(state, arguments)
    api.state_manager.delete_state(state)
    print(f"\nSimulation finished with EnergyPlus status {status}.")


if __name__ == "__main__":
    main()
