import numpy as np
from scipy.optimize import minimize


# 2*(x1 - 6)^2 + 3*(x2 - 6)^2
def f1(x):
    return 2 * (x[0] - 6) ** 2 + 3 * (x[1] - 6) ** 2


# 3*(x1 + 4)^2 + (x2 + 6)^2
def f2(x):
    return 3 * (x[0] + 4) ** 2 + (x[1] + 6) ** 2


# (x1 + 7)^2 + 2*(x2 - 8)^2
def f3(x):
    return (x[0] + 7) ** 2 + 2 * (x[1] - 8) ** 2


initial_point = np.array([0.0, 0.0])

delta_f1_values = np.linspace(5, 50, 5)
delta_f2_values = np.linspace(5, 25, 2)

pareto_points = []

for delta_f1 in delta_f1_values:
    for delta_f2 in delta_f2_values:
        result1 = minimize(f1, initial_point, method='SLSQP')
        x1_optimal = result1.x
        f1_optimal = result1.fun

        constraint1 = {'type': 'ineq', 'fun': lambda x: f1_optimal + delta_f1 - f1(x)}
        result2 = minimize(f2, initial_point, method='SLSQP', constraints=[constraint1])
        x2_optimal = result2.x
        f2_optimal = result2.fun

        constraint2 = {'type': 'ineq', 'fun': lambda x: f1_optimal + delta_f1 - f1(x)}
        constraint3 = {'type': 'ineq', 'fun': lambda x: f2_optimal + delta_f2 - f2(x)}
        result3 = minimize(f3, initial_point, method='SLSQP', constraints=[constraint2, constraint3])
        x3_optimal = result3.x
        f3_optimal = result3.fun

        pareto_points.append({
            'x': x3_optimal,
            'f1': f1(x3_optimal),
            'f2': f2(x3_optimal),
            'f3': f3_optimal,
            'delta_f1': delta_f1,
            'delta_f2': delta_f2
        })

print("Парето-оптимальные точки:")
for i, point in enumerate(pareto_points):
    print(f"\nТочка {i + 1}:")
    print(f"x = {point['x']}")
    print(f"f1 = {point['f1']}")
    print(f"f2 = {point['f2']}")
    print(f"f3 = {point['f3']}")
    print(f"Уступки: delta_f1 = {point['delta_f1']}, delta_f2 = {point['delta_f2']}")
