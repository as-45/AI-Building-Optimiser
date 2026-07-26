"""
Building AI Service

Coordinates the complete AI reasoning pipeline.
"""

from memory.memory_retriever import MemoryRetriever

from llm.prompt.prompt_builder import PromptBuilder

from llm.inference.inference_engine import InferenceEngine

from runtime.decision.decision_engine import DecisionEngine

from runtime.validator.response_validator import ResponseValidator


class BuildingAIService:

    def __init__(self):

        self.memory = MemoryRetriever()

        self.prompt_builder = PromptBuilder()

        self.inference = InferenceEngine()

        self.decision_engine = DecisionEngine()

        self.validator = ResponseValidator()

    # ----------------------------------------------------------

    def analyze(self, building_context):

        """
        Complete AI Pipeline.
        """

        # ------------------------------------
        # Retrieve similar memories
        # ------------------------------------

        memories = []

        # ------------------------------------
        # Build prompt context
        # ------------------------------------

        context = {

            "building": building_context,

            "memories": memories

        }

        prompt = self.prompt_builder.build(

            context

        )

        # ------------------------------------
        # Run Qwen
        # ------------------------------------

        llm_output = self.inference.generate(

            prompt

        )

        # ------------------------------------
        # Convert JSON into Decision object
        # ------------------------------------

        decision = self.decision_engine.build(

            llm_output

        )

        # ------------------------------------
        # Validate
        # ------------------------------------

        validation = self.validator.validate(

            decision

        )

        return {

            "decision": decision,

            "validation": validation

        }