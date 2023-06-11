from graphs import Graphs

added_HIV = True
added_STI = False
added_EXTSHIFT = False

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
