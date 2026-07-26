"""
Current outdoor weather.
"""


class WeatherSection:

    def build(self, context):

        weather = context.weather

        return f"""
==========================
WEATHER
==========================

Outdoor Temperature

{weather["temperature"]:.2f} °C

Outdoor Humidity

{weather["humidity"]:.2f} %
"""