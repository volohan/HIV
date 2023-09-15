'''
from graphs import Graphs

added_HIV = False
added_STI = True
added_EXTSHIFT = True

graphs = Graphs()

# Добавление графика HIV, если True
if added_HIV:
    graphs.add_graphs("HIV", "green", "--")

# Добавление графика STI, если True
if added_STI:
    graphs.add_graphs("STI", "red", "dotted")

# Добавление графика EXTSHIFT, если True
if added_EXTSHIFT:
    graphs.add_graphs("EXTSHIFT", "blue", "-")

# отображение графиков
graphs.show()

'''
import pickle

from matplotlib import pyplot as plt

added_HIV = True
added_STI = True
added_EXTSHIFT = False

# создаем объект фигуры и определяем размер
fig, axes = plt.subplots(nrows=2)

# Добавление подграфиков и настройка параметров
for i in range(2):
    axes[i].set_title(('u_1', 'u_2')[i])

with open('uu.pickle', 'rb') as f:
    graphs = pickle.load(f)
t_1 = []
t_2 = []
for i in range(len(graphs)):
    t_1.extend([graphs[i][0][0]] * 5)
    t_2.extend([graphs[i][0][1]] * 5)

tt = list(range(1, 1001))

axes[0].plot(tt, t_1, "*", color="black")
axes[1].plot(tt, t_2, "*", color="black")

# отображение графиков
plt.show()
