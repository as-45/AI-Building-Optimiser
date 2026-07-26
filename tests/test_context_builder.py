from context.context_builder import ContextBuilder
from context.trend_analyzer import TrendAnalyzer
from memory.memory_retriever import MemoryRetriever

# These will later come from the runtime
building_state = None
history = []
current_episode = None

trigger = {
    "trigger_name": "Comfort",
    "priority": "High",
    "reason": "Comfort degradation detected."
}

builder = ContextBuilder(
    TrendAnalyzer(),
    MemoryRetriever()
)

print("ContextBuilder created successfully.")