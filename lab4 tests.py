import numpy as np


# Определение ограничения g1(x) = 10x1 - x1^2 + 10x2 - x2^2 - 34
def constraint_g1(x):
    """
    Вычисляет значение ограничения g1(x), которое должно быть >= 0.

    Аргументы:
        x : numpy.array - точка [x1, x2]

    Возвращает:
        float - значение g1(x) = 10x1 - x1^2 + 10x2 - x2^2 - 34
    """
    x1, x2 = x
    return 10 * x1 - x1 ** 2 + 10 * x2 - x2 ** 2 - 34


# Исходная целевая функция f(x) = 4x1 - x2^2 - 12
def original_function(x):
    """
    Вычисляет значение целевой функции f(x), которую нужно минимизировать.

    Аргументы:
        x : numpy.array - точка [x1, x2]

    Возвращает:
        float - значение f(x) = 4x1 - x2^2 - 12
    """
    x1, x2 = x
    return 4 * x1 - x2 ** 2 - 12


# Проверка допустимости точки
def is_feasible(x, tol=1e-6):
    """
    Проверяет, находится ли точка внутри допустимой области, где g1(x) > 0, x1 > 0, x2 > 0.

    Аргументы:
        x : numpy.array - точка [x1, x2]
        tol : float - допуск для проверки (чтобы избежать численных ошибок)

    Возвращает:
        bool - True, если точка допустима, False иначе
    """
    x1, x2 = x
    g1 = constraint_g1(x)
    return g1 > tol and x1 > tol and x2 > tol


# Барьерная функция B(x) = -log(g1(x)) - log(x1) - log(x2)
def barrier_function(x):
    """
    Вычисляет значение барьерной функции B(x), которая штрафует за приближение к границам.

    Аргументы:
        x : numpy.array - точка [x1, x2]

    Возвращает:
        float - значение B(x), если точка допустима

    Исключения:
        ValueError - если точка нарушает ограничения
    """
    if not is_feasible(x):
        raise ValueError("Точка находится вне допустимой области: g1(x) <= 0 или x1, x2 <= 0")
    x1, x2 = x
    g1 = constraint_g1(x)
    return -np.log(g1) - np.log(x1) - np.log(x2)


# Градиент исходной функции f(x)
def gradient_original(x):
    """
    Вычисляет градиент функции f(x) = 4x1 - x2^2 - 12.

    Аргументы:
        x : numpy.array - точка [x1, x2]

    Возвращает:
        numpy.array - градиент [df/dx1, df/dx2] = [4, -2 * x2]
    """
    x1, x2 = x
    df_dx1 = 4
    df_dx2 = -2 * x2
    return np.array([df_dx1, df_dx2])


# Градиент барьерной функции B(x)
def gradient_barrier(x):
    """
    Вычисляет градиент барьерной функции B(x) = -log(g1(x)) - log(x1) - log(x2).

    Аргументы:
        x : numpy.array - точка [x1, x2]

    Возвращает:
        numpy.array - градиент [dB/dx1, dB/dx2]

    Исключения:
        ValueError - если точка нарушает ограничения
    """
    if not is_feasible(x):
        raise ValueError("Точка находится вне допустимой области: g1(x) <= 0 или x1, x2 <= 0")
    x1, x2 = x
    g1 = constraint_g1(x)
    dg1_dx1 = 10 - 2 * x1  # dg1/dx1
    dg1_dx2 = 10 - 2 * x2  # dg1/dx2
    grad_b_x1 = -(dg1_dx1 / g1) - (1 / x1)
    grad_b_x2 = -(dg1_dx2 / g1) - (1 / x2)
    return np.array([grad_b_x1, grad_b_x2])


# Градиент обновленной функции phi(x) = f(x) + M * B(x)
def gradient_updated(x, M):
    """
    Вычисляет градиент функции phi(x) = f(x) + M * B(x).

    Аргументы:
        x : numpy.array - точка [x1, x2]
        M : float - параметр барьерной функции

    Возвращает:
        numpy.array - градиент [dphi/dx1, dphi/dx2]
    """
    grad_f = gradient_original(x)
    grad_b = gradient_barrier(x)
    return grad_f + M * grad_b


# Параметры алгоритма
initial_point = np.array([2.0, 4.0])  # Начальная точка x^0
alpha = 0.001  # Уменьшенный шаг градиентного спуска для стабильности
M = 1000  # Параметр барьерной функции
epsilon = 0.05  # Критерий сходимости
num_iterations = 3  # Количество итераций
max_alpha_attempts = 5  # Максимальное количество попыток уменьшения шага

# Основной цикл градиентного спуска
current_point = initial_point.copy()
print(
    f"Итерация 0: x = {current_point}, f(x) = {original_function(current_point)}, g1(x) = {constraint_g1(current_point)}")

for iteration in range(num_iterations):
    # Вычисляем градиент в текущей точке
    grad = gradient_updated(current_point, M)

    # Пробуем обновить точку с текущим шагом alpha
    alpha_current = alpha
    for attempt in range(max_alpha_attempts):
        next_point = current_point - alpha_current * grad
        # Проверяем, является ли новая точка допустимой
        if is_feasible(next_point):
            break
        else:
            # Если точка недопустима, уменьшаем шаг
            alpha_current *= 0.5
            print(
                f"Итерация {iteration + 1}, попытка {attempt + 1}: точка недопустима, уменьшаем шаг до alpha = {alpha_current}")
            if attempt == max_alpha_attempts - 1:
                print(f"Итерация {iteration + 1}: не удалось найти допустимую точку после {max_alpha_attempts} попыток")
                break

    # Обновляем точку
    next_point = current_point - alpha_current * grad
    f_old = original_function(current_point)
    f_new = original_function(next_point)
    diff = abs(f_new - f_old)

    # Выводим результаты
    print(
        f"Итерация {iteration + 1}: x = {next_point}, f(x) = {f_new}, |f(x_new) - f(x_old)| = {diff}, g1(x) = {constraint_g1(next_point)}")

    # Проверяем критерий сходимости
    if diff < epsilon:
        print(f"Критерий сходимости выполнен: |f(x_new) - f(x_old)| < {epsilon}")
        break

    current_point = next_point

print(f"Финальная точка после {num_iterations} итераций: x = {current_point}")