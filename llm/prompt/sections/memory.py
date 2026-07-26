"""
Adds retrieved memories into the prompt.
"""


class MemorySection:

    def build(self, context):

        text = """
==========================
SIMILAR PAST EPISODES
==========================

"""

        memories = context.retrieved_memories

        if len(memories) == 0:

            text += "No similar building episodes were found.\n"

            return text

        for i, memory in enumerate(memories, start=1):

            text += f"""
Episode {i}

Similarity Distance:
{memory["distance"]:.4f}

Summary

{memory["document"]}

-------------------------------------

"""

        return text