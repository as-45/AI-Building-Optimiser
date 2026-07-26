"""
Trigger section.
"""


class TriggerSection:

    def build(self, context):

        trigger = context.trigger

        return f"""
==========================================================
TRIGGER
==========================================================

Trigger Name

{trigger.get("trigger", "Unknown")}

Priority

{trigger.get("priority", "Normal")}

Reason

{trigger.get("reason", "Not Specified")}

Confidence

{trigger.get("confidence", 1.0):.2f}
"""