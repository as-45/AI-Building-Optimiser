"""
context_formatter.py

Formats all prompt sections into one final prompt.
"""


class ContextFormatter:

    def format(self, sections):

        return "\n\n".join(sections)