import numpy as np

A = np.array([[2, -1]])
b = 2

AAT = A @ A.T
P = np.eye(2) - (A.T @ A) / AAT


def grad_f(x):
    return np.array([2 * x[0], -2 * x[1]])


x = np.array([0.0, -2.0])

if not np.allclose(A @ x, b):
    raise ValueError("Начальная точка не удовлетворяет ограничению")

epsilon = 1e-6
max_iter = 100

for i in range(max_iter):
    grad = grad_f(x)
    d = -P @ grad
    if np.linalg.norm(d) < epsilon:
        print(f"Сошелся после {i} итераций")
        break
    numerator = x[0] * d[0] - x[1] * d[1]
    denominator = d[1] ** 2 - d[0] ** 2
    alpha = numerator / denominator
    x = x + alpha * d
else:
    print("Не сошелся за максимальное число итераций")

print("Оптимальная точка:", x)
print("Значение целевой функции:", x[0] ** 2 - x[1] ** 2)
