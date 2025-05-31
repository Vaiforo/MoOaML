import numpy as np


# g1(x) = 10x1 - x1^2 + 10x2 - x2^2 - 34
def constraint_g1(x):
    x1, x2 = x
    return 10 * x1 - x1 ** 2 + 10 * x2 - x2 ** 2 - 34


# f(x) = 4x1 - x2^2 - 12
def original_function(x):
    x1, x2 = x
    return 4 * x1 - x2 ** 2 - 12


def is_feasible(x, tol=1e-6):
    x1, x2 = x
    g1 = constraint_g1(x)
    return g1 > tol and x1 > tol and x2 > tol


# B(x) = -log(g1(x)) - log(x1) - log(x2)
def barrier_function(x):
    if not is_feasible(x):
        raise ValueError("Точка находится вне допустимой области: g1(x) <= 0 или x1, x2 <= 0")
    x1, x2 = x
    g1 = constraint_g1(x)
    return -np.log(g1) - np.log(x1) - np.log(x2)


def gradient_original(x):
    x1, x2 = x
    df_dx1 = 4
    df_dx2 = -2 * x2
    return np.array([df_dx1, df_dx2])


def gradient_barrier(x):
    if not is_feasible(x):
        raise ValueError("Точка находится вне допустимой области: g1(x) <= 0 или x1, x2 <= 0")
    x1, x2 = x
    g1 = constraint_g1(x)
    dg1_dx1 = 10 - 2 * x1
    dg1_dx2 = 10 - 2 * x2
    grad_b_x1 = -(dg1_dx1 / g1) - (1 / x1)
    grad_b_x2 = -(dg1_dx2 / g1) - (1 / x2)
    return np.array([grad_b_x1, grad_b_x2])


# phi(x) = f(x) + M * B(x)
def gradient_updated(x, M):
    grad_f = gradient_original(x)
    grad_b = gradient_barrier(x)
    return grad_f + M * grad_b


initial_point = np.array([2.0, 4.0])
alpha = 0.001
M = 1000
epsilon = 0.05
num_iterations = 3
max_alpha_attempts = 5

current_point = initial_point.copy()
print(
    f"Итерация 0: x = {current_point}, f(x) = {original_function(current_point)}, g1(x) = {constraint_g1(current_point)}")

for iteration in range(num_iterations):
    grad = gradient_updated(current_point, M)

    alpha_current = alpha
    for attempt in range(max_alpha_attempts):
        next_point = current_point - alpha_current * grad
        if is_feasible(next_point):
            break
        else:
            alpha_current *= 0.5
            print(
                f"Итерация {iteration + 1}, попытка {attempt + 1}: точка недопустима, уменьшаем шаг до alpha = {alpha_current}")
            if attempt == max_alpha_attempts - 1:
                print(f"Итерация {iteration + 1}: не удалось найти допустимую точку после {max_alpha_attempts} попыток")
                break

    next_point = current_point - alpha_current * grad
    f_old = original_function(current_point)
    f_new = original_function(next_point)
    diff = abs(f_new - f_old)

    print(
        f"Итерация {iteration + 1}: x = {next_point}, f(x) = {f_new}, |f(x_new) - f(x_old)| = {diff}, g1(x) = {constraint_g1(next_point)}")

    if diff < epsilon:
        print(f"Критерий сходимости выполнен: |f(x_new) - f(x_old)| < {epsilon}")
        break

    current_point = next_point

print(f"Финальная точка после {num_iterations} итераций: x = {current_point}")