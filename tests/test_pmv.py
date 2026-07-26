from metrics.pmv import PMVEngine

engine = PMVEngine()

result = engine.evaluate(

    air_temperature=25,

    relative_humidity=50

)

print(result)