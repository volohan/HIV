import pickle

from matplotlib import pyplot as plt
from HIV import T1, T2, I1, I2, V, E, start, t0, tn, h
from RK4 import RK4


def draw(t, f1, f2, f3, f4, f5, f6):
    STI = []
    with open('STI.pickle', 'rb') as f:
        STI = pickle.load(f)
    x, y = RK4([T1, T2, I1, I2, V, E], start, t0, tn, h)
    # создаем объект фигуры и определяем размер
    fig = plt.figure(figsize=(10, 8))

    # добавляем первый подграфик
    ax1 = fig.add_subplot(3, 2, 1)  # 2 строки, 3 столбца, 1-ый подграфик
    ax1.plot(t, f1)
    ax1.plot(STI[0], STI[1], color='green')
    ax1.plot(x, [yi[0] for yi in y], color='red', linestyle='dashed')
    ax1.set_title('T1')
    ax1.set_yscale('log')

    # добавляем второй подграфик
    ax2 = fig.add_subplot(3, 2, 2)  # 2 строки, 3 столбца, 2-ой подграфик
    ax2.plot(t, f2)
    ax2.plot(STI[0], STI[2], color='green')
    ax2.plot(x, [yi[1] for yi in y], color='red', linestyle='dashed')
    ax2.set_title('T2')
    ax2.set_yscale('log')

    # добавляем третий подграфик
    ax3 = fig.add_subplot(3, 2, 3)  # 2 строки, 3 столбца, 3-ий подграфик
    ax3.plot(t, f3)
    ax3.plot(STI[0], STI[3], color='green')
    ax3.plot(x, [yi[2] for yi in y], color='red', linestyle='dashed')
    ax3.set_title('I1')
    ax3.set_yscale('log')

    # добавляем четвертый подграфик
    ax4 = fig.add_subplot(3, 2, 4)  # 2 строки, 3 столбца, 4-ый подграфик
    ax4.plot(t, f4)
    ax4.plot(STI[0], STI[4], color='green')
    ax4.plot(x, [yi[3] for yi in y], color='red', linestyle='dashed')
    ax4.set_title('I2')
    ax4.set_yscale('log')

    # добавляем пятый подграфик
    ax5 = fig.add_subplot(3, 2, 5)  # 2 строки, 3 столбца, 5-ый подграфик
    ax5.plot(t, f5)
    ax5.plot(STI[0], STI[5], color='green')
    ax5.plot(x, [yi[4] for yi in y], color='red', linestyle='dashed')
    ax5.set_title('V')
    ax5.set_yscale('log')

    # добавляем шестой подграфик
    ax6 = fig.add_subplot(3, 2, 6)  # 2 строки, 3 столбца, 6-ой подграфик
    ax6.plot(t, f6)
    ax6.plot(STI[0], STI[6], color='green')
    ax6.plot(x, [yi[5] for yi in y], color='red', linestyle='dashed')
    ax6.set_title('E')
    ax6.set_yscale('log')

    plt.show()
