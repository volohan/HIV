from RK4 import RK4
import matplotlib.pyplot as plt

start = [163573, 5, 11945, 46, 63919, 24]
t0, tn, h = (0, 1000, 0.01)

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


if __name__ == '__main__':
    x, y = RK4([T1, T2, I1, I2, V, E], start, t0, tn, h)

    # создаем объект фигуры и определяем размер
    fig = plt.figure(figsize=(10, 8))

    # добавляем первый подграфик
    ax1 = fig.add_subplot(3, 2, 1)  # 2 строки, 3 столбца, 1-ый подграфик
    ax1.plot(x, [yi[0] for yi in y])
    ax1.set_title('T1')
    ax1.set_yscale('log')

    # добавляем второй подграфик
    ax2 = fig.add_subplot(3, 2, 2)  # 2 строки, 3 столбца, 2-ой подграфик
    ax2.plot(x, [yi[1] for yi in y])
    ax2.set_title('T2')
    ax2.set_yscale('log')

    # добавляем третий подграфик
    ax3 = fig.add_subplot(3, 2, 3)  # 2 строки, 3 столбца, 3-ий подграфик
    ax3.plot(x, [yi[2] for yi in y])
    ax3.set_title('I1')
    ax3.set_yscale('log')

    # добавляем четвертый подграфик
    ax4 = fig.add_subplot(3, 2, 4)  # 2 строки, 3 столбца, 4-ый подграфик
    ax4.plot(x, [yi[3] for yi in y])
    ax4.set_title('I2')
    ax4.set_yscale('log')

    # добавляем пятый подграфик
    ax5 = fig.add_subplot(3, 2, 5)  # 2 строки, 3 столбца, 5-ый подграфик
    ax5.plot(x, [yi[4] for yi in y])
    ax5.set_title('V')
    ax5.set_yscale('log')

    # добавляем шестой подграфик
    ax6 = fig.add_subplot(3, 2, 6)  # 2 строки, 3 столбца, 6-ой подграфик
    ax6.plot(x, [yi[5] for yi in y])
    ax6.set_title('E')
    ax6.set_yscale('log')

    plt.show()
