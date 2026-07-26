"""
Builds the trend section of the prompt.
"""


class TrendSection:

    def build(self, context):

        trend = context.trend_report

        return f"""
==========================
BUILDING TRENDS
==========================

Outdoor Temperature Trend:
{trend.temperature_trend}

Comfort Trend:
{trend.comfort_trend}

HVAC Trend:
{trend.hvac_trend}

Building Power Trend:
{trend.power_trend}

Carbon Trend:
{trend.carbon_trend}

Predicted Building Power:
{trend.predicted_power:.2f} W

Predicted HVAC Power:
{trend.predicted_hvac:.2f} W

Predicted Comfort:
{trend.predicted_comfort:.2f}
"""