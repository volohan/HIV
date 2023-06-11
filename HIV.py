import pickle
from RK4 import RK4

lambda_1 = 10000
lambda_2 = 31.98
d_1 = 0.01
d_2 = 0.01
k_1 = 8 * 10 ** (-7)
k_2 = 0.0001
delta = 0.7
m_1 = 0.00001
m_2 = 0.00001
N_T = 100
c = 13
ro_1 = 1
ro_2 = 1
lambda_E = 1
delta_E = 0.1
b_E = 0.3
d_E = 0.25
K_b = 100
K_d = 500
f = 0.35

'''
# функция правой части дифференциального уравнения (y' = f(x, y))
def f1(t,u_1, u_2, T_1, T_2, I_1, I_2, V, E):
    return lambda_1 - d_1 * T_1 - (1 - u_1) * k_1 * V * T_1
def f2(t, u_1, u_2, T_1, T_2, I_1, I_2, V, E):
    return lambda_2 - d_2 * T_2 - (1 - f * u_1) * k_2 * V * T_2
def f3(t, u_1, u_2, T_1, T_2, I_1, I_2, V, E):
    return (1 - u_1) * k_1 * V * T_1 - delta * I_1 - m_1 * E * I_1
def f4(t, u_1, u_2, T_1, T_2, I_1, I_2, V, E):
    return (1 - f * u_1) * k_2 * V * T_2 - delta * I_2 - m_2 * E * I_2
def f5(t, u_1, u_2, T_1, T_2, I_1, I_2, V, E):
    return (1 - u_2) * N_T * delta * (I_1 + I_2) - c * V - ((1 - u_1) * ro_1 * k_1 * T_1 + (1 - f * u_1) * ro_2 * k_2 * T_2) * V
def f6(t, u_1, u_2, T_1, T_2, I_1, I_2, V, E):
    return lambda_E + (b_E * (I_1 + I_2)) / ((I_1 + I_2) + K_b) * E - (d_E * (I_1 + I_2)) / ((I_1 + I_2) + K_d) * E - delta_E * E
'''


# функция правой части дифференциального уравнения (y' = f(x, y))
def T1(t, T_1, T_2, I_1, I_2, V, E, u_1=0.7, u_2=0.3):
    return lambda_1 - d_1 * T_1 - (1 - u_1) * k_1 * V * T_1


def T2(t, T_1, T_2, I_1, I_2, V, E, u_1=0.7, u_2=0.3):
    return lambda_2 - d_2 * T_2 - (1 - f * u_1) * k_2 * V * T_2


def I1(t, T_1, T_2, I_1, I_2, V, E, u_1=0.7, u_2=0.3):
    return (1 - u_1) * k_1 * V * T_1 - delta * I_1 - m_1 * E * I_1


def I2(t, T_1, T_2, I_1, I_2, V, E, u_1=0.7, u_2=0.3):
    return (1 - f * u_1) * k_2 * V * T_2 - delta * I_2 - m_2 * E * I_2


def V(t, T_1, T_2, I_1, I_2, V, E, u_1=0.7, u_2=0.3):
    return (1 - u_2) * N_T * delta * (I_1 + I_2) - c * V - (
            (1 - u_1) * ro_1 * k_1 * T_1 + (
            1 - f * u_1) * ro_2 * k_2 * T_2) * V


def E(t, T_1, T_2, I_1, I_2, V, E, u_1=0.7, u_2=0.3):
    return lambda_E + (b_E * (I_1 + I_2)) / ((I_1 + I_2) + K_b) * E - (
            d_E * (I_1 + I_2)) / ((I_1 + I_2) + K_d) * E - delta_E * E


def compute(u1, u2, tn):
    start = [163573, 5, 11945, 46, 63919, 24]
    t0, h = (0, 0.01)

    # Решение уравнения методом Рунге-Кутты и получение значений функций
    x, y = RK4([T1, T2, I1, I2, V, E], start, t0, [u1, u2], tn, h)

    # Создание списка списков для значений функций
    f = [[] for _ in range(len(y[0]))]

    # Добавление значений функций в соответствующие списки
    for yi in y:
        for i, fi in enumerate(yi):
            f[i].append(fi)

    # Сохранение графиков фазовых переменных
    with open('HIV.pickle', 'wb') as p:
        pickle.dump([x, *f], p)


if __name__ == '__main__':
    compute(0.7, 0.3, 1000)
