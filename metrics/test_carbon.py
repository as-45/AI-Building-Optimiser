from carbon import evaluate_carbon

tests = [

    55826,

    54000,

    52000,

    49000,

    60000

]

for value in tests:

    print("="*70)

    print(evaluate_carbon(value))