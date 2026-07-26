from energy import evaluate_energy

tests = [

    55826,

    54000,

    52000,

    49000,

    60000

]

for value in tests:

    print("="*60)

    print(evaluate_energy(value))