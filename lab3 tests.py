import numpy as np

# Определение матрицы ограничения A и вектора b
A = np.array([[2, -1]])
b = 2

# Вычисление матрицы проекции P
AAT = A @ A.T
P = np.eye(2) - (A.T @ A) / AAT


# Определение градиента целевой функции
def grad_f(x):
    return np.array([2 * x[0], -2 * x[1]])


# Начальная точка, удовлетворяющая ограничению
x = np.array([0.0, -2.0])

# Проверка начальной точки
if not np.allclose(A @ x, b):
    raise ValueError("Начальная точка не удовлетворяет ограничению")

# Параметры: точность и максимальное число итераций
epsilon = 1e-6
max_iter = 100

for i in range(max_iter):
    grad = grad_f(x)
    d = -P @ grad
    if np.linalg.norm(d) < epsilon:
        print(f"Сошелся после {i} итераций")
        break
    # Вычисление шага alpha
    numerator = x[0] * d[0] - x[1] * d[1]
    denominator = d[1] ** 2 - d[0] ** 2
    alpha = numerator / denominator
    x = x + alpha * d
else:
    print("Не сошелся за максимальное число итераций")

# Вывод результата
print("Оптимальная точка:", x)
print("Значение целевой функции:", x[0] ** 2 - x[1] ** 2)
