import pickle
from matplotlib import pyplot as plt


class Graphs:
    def __init__(self):
        # создаем объект фигуры и определяем размер
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = []

        # Добавление подграфиков и настройка параметров
        for i in range(1, 7):
            ax = self.fig.add_subplot(3, 2, i)
            ax.set_title(('T1', 'T2', 'I1', 'I2', 'V', 'E')[i - 1])
            ax.set_yscale('log')
            self.ax.append(ax)

    def add_graphs(self, name, color='blue', linestyle='-'):
        # Открытие файла с данными фазовых переменных
        with open(f'{name}.pickle', 'rb') as f:
            graphs = pickle.load(f)

        # Построение графиков
        for i, ax in enumerate(self.ax):
            ax.plot(graphs[0], graphs[i + 1], color=color, linestyle=linestyle)

    def show(self):
        plt.show()


def show_plot(added_HIV, added_STI, added_EXTSHIFT, color1, style1, color2,
              style2, color3, style3):
    '''
    added_HIV = True
    added_STI = False
    added_EXTSHIFT = False
    '''

    graphs = Graphs()

    # Добавление графика HIV, если True
    if added_HIV:
        graphs.add_graphs("HIV", color1, style1)

    # Добавление графика STI, если True
    if added_STI:
        graphs.add_graphs("STI", color2, style2)

    # Добавление графика EXTSHIFT, если True
    if added_EXTSHIFT:
        graphs.add_graphs("EXTSHIFT", color3, style3)

    # отображение графиков
    graphs.show()
