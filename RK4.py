import numpy as np


# метод Рунге-Кутта 4-го порядка
def RK4(f, y0, x0, u, xn, h):
    # y0 - начальное условие (значение y(x0))
    # x0 - начальное значение
    # xn - конечное значение
    # h - шаг

    if not isinstance(f, list):
        f = [f]
    if not isinstance(y0, list):
        y0 = [y0]

    x = np.arange(x0, xn + h, h)  # массив значений x
    y = np.zeros((len(x), len(f)))  # массив значений y
    y[0] = y0  # вводим начальное значение

    # Инициализация временных переменных
    k1 = np.zeros(len(f))
    k2 = np.zeros(len(f))
    k3 = np.zeros(len(f))
    k4 = np.zeros(len(f))
    temp1 = np.zeros(len(f))
    temp2 = np.zeros(len(f))
    temp3 = np.zeros(len(f))

    # Реализация метода Рунге-Кутты 4-го порядка
    for i in range(len(x) - 1):
        # Подсчет k1
        for j in range(len(f)):
            k1[j] = h * f[j](x[i], *y[i], *u)
            temp1[j] = y[i][j] + k1[j] / 2
        # Подсчет k2
        for j in range(len(f)):
            k2[j] = h * f[j](x[i] + h / 2, *temp1, *u)
            temp2[j] = y[i][j] + k2[j] / 2
        # Подсчет k3
        for j in range(len(f)):
            k3[j] = h * f[j](x[i] + h / 2, *temp2, *u)
            temp3[j] = y[i][j] + k3[j]
        # Подсчет k4
        for j in range(len(f)):
            k4[j] = h * f[j](x[i] + h, *temp3, *u)
        # Подсчет узла (i+1)
        for j in range(len(f)):
            y[i + 1][j] = y[i][j] + (1 / 6) * (
                    k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j])

    return x, y
