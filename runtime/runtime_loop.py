"""
runtime_loop.py

Main autonomous control loop.

Flow:

EnergyPlus
      ↓
BuildingState
      ↓
Live Metrics
      ↓
Context Builder
      ↓
MCP Server (RunPod)
      ↓
Qwen3-8B
      ↓
Decision
      ↓
Validator
      ↓
Executor
      ↓
EnergyPlus
"""

from metrics.live_metrics_engine import LiveMetricsEngine
from context.context_builder import ContextBuilder


class RuntimeLoop:

    def __init__(
        self,
        trend_analyzer,
        memory_retriever,
        mcp_client,
        executor
    ):

        self.metrics_engine = LiveMetricsEngine()

        self.context_builder = ContextBuilder(
            trend_analyzer,
            memory_retriever
        )

        self.mcp_client = mcp_client
        self.executor = executor

    # ----------------------------------------------------

    def run_step(
        self,
        building_state,
        history,
        current_episode,
        trigger,
        callback_number=0
    ):
        """
        Executes one autonomous control cycle.
        """

        # ------------------------------------
        # Evaluate live metrics
        # ------------------------------------

        metrics = self.metrics_engine.evaluate(
            building_state
        )

        # ------------------------------------
        # Build LLM context
        # ------------------------------------

        context = self.context_builder.build(
            building_state,
            history,
            current_episode,
            trigger
        )

        # ------------------------------------
        # Ask the AI
        # ------------------------------------

        decision = self.mcp_client.analyze_building(
            context.__dict__
        )

        # ------------------------------------
        # Execute returned actions
        # ------------------------------------

        execution = self.executor.execute(
            decision,
            callback_number
        )

        return {
            "metrics": metrics,
            "decision": decision,
            "execution": execution
        }
