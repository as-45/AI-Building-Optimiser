from hvac import HVACMetric
from comfort import evaluate_comfort

hvac = HVACMetric()

tests = [

    (20000, 24),

    (18000, 24),

    (15000, 24),

    (25000, 24),

    (15000, 29),

    (25000, 29)

]

for hvac_power, temperature in tests:

    comfort = evaluate_comfort(temperature)

    result = hvac.evaluate(

        current_hvac_power=hvac_power,

        current_temperature=temperature,

        comfort_result=comfort

    )

    print("=" * 70)

    print(result)