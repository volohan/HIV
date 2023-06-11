import pickle
import re
import time

import EXTSHIFT
import HIV
import graphs
import STI
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, \
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QComboBox, QTabWidget, QGroupBox, QCheckBox, QProgressBar
from PyQt5.QtCore import QRegExp, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QRegExpValidator


class ComputeThread(QThread):
    progress_changed = pyqtSignal(str, int)

    def __init__(self, gui):
        super().__init__(parent=gui)
        self.progress = 0
        self.gui = gui

    def run(self):
        u1_max = float(self.gui.u1_edit.text())
        u2_max = float(self.gui.u2_edit.text())
        tf = int(self.gui.tf_edit.text())
        l = int(self.gui.l_edit.text())
        s = int(self.gui.s_edit.text())

        if self.gui.hiv_checkbox.isChecked():
            self.progress_changed.emit("HIV: model compute start", 0)
            HIV.compute(u1_max, u2_max, tf)
            self.progress_changed.emit("HIV: model compute end", tf)
            self.sleep(2)
        if self.gui.sti_checkbox.isChecked():
            self.progress_changed.emit("STI: metod compute start", 0)
            self.sleep(2)
            STI.STI(u1_max, u2_max, tf, s, l, self.progress_changed)
            self.progress_changed.emit("STI: model compute end", tf)
            self.sleep(2)
        if self.gui.extshift_checkbox.isChecked():
            self.progress_changed.emit("EXTSHIFT: metod compute start", 0)
            self.sleep(2)
            EXTSHIFT.compute(u1_max, u2_max, self.progress_changed)
            self.progress_changed.emit("EXTSHIFT: model compute end", tf)
            self.sleep(2)

        self.progress_changed.emit("FINISHED!", tf)


class MainWindow(QMainWindow):

    def __init__(self, setting):
        super().__init__()
        self.setting = setting
        self.initUI()

    # Функция, которая создает UI
    def initUI(self):
        # Создаем виджет
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Создаем таббар
        tabbar = QTabWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(tabbar)
        up_widget = QWidget()
        up_widget.setLayout(main_layout)
        self.widget.setLayout(QVBoxLayout())
        self.widget.layout().addWidget(up_widget)

        # Создаем первый таб
        tab1 = QWidget()
        tabbar.addTab(tab1, "Стиль")

        # Создаем элементы первого таба
        hiv_label = QLabel("При максимальном управлении:")
        hiv_label.setFixedSize(250, 20)
        sti_label = QLabel("Траектория Z-поводыря:")
        sti_label.setFixedSize(250, 20)
        extshift_label = QLabel("Движение X-объекта:")
        extshift_label.setFixedSize(250, 20)

        # Создаем поля для выбора цвета и стиля
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink',
                  'gray', 'olive', 'cyan']
        styles = ['solid', 'dashed', 'dashdot', 'dotted']
        self.color_combo1 = QComboBox()
        self.color_combo1.addItems(colors)
        self.color_combo1.setCurrentText(self.setting["hiv"][0])
        self.color_combo1.currentTextChanged.connect(
            lambda: self.update_setting("hiv", (
                self.color_combo1.currentText(), self.setting["hiv"][1])))
        self.style_combo1 = QComboBox()
        self.style_combo1.addItems(styles)
        self.style_combo1.setCurrentText(self.setting["hiv"][1])
        self.style_combo1.currentTextChanged.connect(
            lambda: self.update_setting("hiv", (
                self.setting["hiv"][0], self.style_combo1.currentText())))
        self.color_combo2 = QComboBox()
        self.color_combo2.addItems(colors)
        self.color_combo2.setCurrentText(self.setting["sti"][0])
        self.color_combo2.currentTextChanged.connect(
            lambda: self.update_setting("sti", (
                self.color_combo2.currentText(), self.setting["sti"][1])))
        self.style_combo2 = QComboBox()
        self.style_combo2.addItems(styles)
        self.style_combo2.setCurrentText(self.setting["sti"][1])
        self.style_combo2.currentTextChanged.connect(
            lambda: self.update_setting("sti", (
                self.setting["sti"][0], self.style_combo2.currentText())))
        self.color_combo3 = QComboBox()
        self.color_combo3.addItems(colors)
        self.color_combo3.setCurrentText(self.setting["extshift"][0])
        self.color_combo3.currentTextChanged.connect(
            lambda: self.update_setting("extshift", (
                self.color_combo1.currentText(), self.setting["extshift"][1])))
        self.style_combo3 = QComboBox()
        self.style_combo3.addItems(styles)
        self.style_combo3.setCurrentText(self.setting["extshift"][1])
        self.style_combo3.currentTextChanged.connect(
            lambda: self.update_setting("extshift", (
                self.setting["extshift"][0], self.style_combo3.currentText())))

        # Создаем vbox для вертикальной компоновки
        vbox_tab1 = QVBoxLayout()

        # Создаем hbox для горизонтальной компоновки
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        # Добавляем элементы в hbox
        hbox1.addWidget(hiv_label)
        hbox1.addWidget(self.color_combo1)
        hbox1.addWidget(self.style_combo1)
        hbox1.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Minimum))
        hbox2.addWidget(sti_label)
        hbox2.addWidget(self.color_combo2)
        hbox2.addWidget(self.style_combo2)
        hbox2.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Minimum))
        hbox3.addWidget(extshift_label)
        hbox3.addWidget(self.color_combo3)
        hbox3.addWidget(self.style_combo3)
        hbox3.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Minimum))

        # Добавляем hboxs в vbox
        vbox_tab1.addLayout(hbox1)
        vbox_tab1.addLayout(hbox2)
        vbox_tab1.addLayout(hbox3)
        vbox_tab1.addSpacerItem(
            QSpacerItem(0, 30, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Добавляем vbox в первый таб
        tab1.setLayout(vbox_tab1)

        # Создаем второй таб
        tab2 = QWidget()
        tabbar.addTab(tab2, "Значения")

        # Создаем элементы второго таба
        u1_label = QLabel("Лечение u1:")
        u1_label.setFixedSize(100, 20)
        u2_label = QLabel("Лечение u2:")
        u2_label.setFixedSize(100, 20)
        tf_label = QLabel("Время tf:")
        tf_label.setFixedSize(100, 20)
        s_label = QLabel("Период s:")
        s_label.setFixedSize(100, 20)
        l_label = QLabel("Подпериод l:")
        l_label.setFixedSize(100, 20)
        self.u1_edit = QLineEdit()
        self.u1_edit.setValidator(QRegExpValidator(QRegExp(r"^[0-9\.]*$")))
        self.u1_edit.setText(self.setting["u1"])
        self.u1_edit.editingFinished.connect(
            lambda: self.check_input_float(self.u1_edit, "u1"))
        self.u2_edit = QLineEdit()
        self.u2_edit.setValidator(QRegExpValidator(QRegExp(r"^[0-9\.]*$")))
        self.u2_edit.setText(self.setting["u2"])
        self.u2_edit.editingFinished.connect(
            lambda: self.check_input_float(self.u2_edit, "u2"))
        self.tf_edit = QLineEdit()
        self.tf_edit.setValidator(QRegExpValidator(QRegExp(r"^(?!0)\d+$")))
        self.tf_edit.setText(self.setting["tf"])
        self.tf_edit.editingFinished.connect(
            lambda: self.update_setting("tf", self.tf_edit.text()))
        self.l_edit = QLineEdit()
        self.l_edit.setValidator(QRegExpValidator(QRegExp(r"^(?!0)\d+$")))
        self.l_edit.setText(self.setting["l"])
        self.l_edit.editingFinished.connect(
            lambda: self.update_setting("l", self.l_edit.text()))
        self.s_edit = QLineEdit()
        self.s_edit.setValidator(QRegExpValidator(QRegExp(r"^(?!0)\d+$")))
        self.s_edit.setText(self.setting["s"])
        self.s_edit.editingFinished.connect(
            lambda: self.update_setting("s", self.s_edit.text()))

        # Создаем vbox для вертикальной компоновки второго таба
        vbox_2 = QVBoxLayout()

        # Создаем hbox для горизонтальной компоновки элементов второго таба
        hbox1_2 = QHBoxLayout()
        hbox2_2 = QHBoxLayout()
        hbox3_2 = QHBoxLayout()
        hbox4_2 = QHBoxLayout()
        hbox5_2 = QHBoxLayout()

        # Добавляем элементы в hboxs
        hbox1_2.addWidget(u1_label)
        hbox1_2.addWidget(self.u1_edit)
        hbox1_2.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Minimum))
        hbox2_2.addWidget(u2_label)
        hbox2_2.addWidget(self.u2_edit)
        hbox2_2.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Minimum))
        hbox3_2.addWidget(tf_label)
        hbox3_2.addWidget(self.tf_edit)
        hbox3_2.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Maximum))
        hbox4_2.addWidget(l_label)
        hbox4_2.addWidget(self.l_edit)
        hbox4_2.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Maximum))
        hbox5_2.addWidget(s_label)
        hbox5_2.addWidget(self.s_edit)
        hbox5_2.addSpacerItem(
            QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Maximum))

        # Добавляем hboxs в vbox второго таба
        vbox_2.addLayout(hbox1_2)
        vbox_2.addLayout(hbox2_2)
        vbox_2.addLayout(hbox3_2)
        vbox_2.addLayout(hbox4_2)
        vbox_2.addLayout(hbox5_2)
        vbox_2.addSpacerItem(
            QSpacerItem(0, 30, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Устанавливаем vbox на второй таб
        tab2.setLayout(vbox_2)

        # Создаем группу чекбоксов
        groupbox = QGroupBox("Графики фазовых переменных")
        self.hiv_checkbox = QCheckBox("При максимальном управлении")
        self.sti_checkbox = QCheckBox("Траектория Z-поводыря")
        self.extshift_checkbox = QCheckBox("Движение X-объекта")

        # Добавляем чекбоксы в группу
        groupbox_layout = QVBoxLayout()
        groupbox_layout.addWidget(self.hiv_checkbox)
        groupbox_layout.addWidget(self.sti_checkbox)
        groupbox_layout.addWidget(self.extshift_checkbox)

        # Устанавливаем группу в форму
        groupbox.setLayout(groupbox_layout)

        # Создаем кнопку
        self.plot_button = QPushButton("Отобразить графики")

        # Добавляем форму и кнопку в widget
        right_widget = QWidget()
        vbox_3 = QVBoxLayout()
        vbox_3.addWidget(groupbox)
        vbox_3.addWidget(self.plot_button)
        right_widget.setLayout(vbox_3)
        main_layout.addWidget(right_widget)

        # Добавляем действие кнопок
        self.plot_button.clicked.connect(self.plot)

        self.progressbar = None
        self.thread = None

        # Устанавливаем заголовок
        self.setWindowTitle("EXTSHIFT")

    # Функция, которая вызывается при нажатии на кнопку "Отобразить графики"
    def plot(self):
        print("button press")
        if not self.progressbar:
            self.progresslabel = QLabel()
            self.progressbar = QProgressBar()
            self.progressbar.setMaximum(int(self.tf_edit.text()))
            self.widget.layout().addWidget(self.progresslabel)
            self.widget.layout().addWidget(self.progressbar)
        print("progress bar init")

        if self.thread:
            self.thread.terminate()
            self.thread = None

        self.thread = ComputeThread(self)
        self.thread.progress_changed.connect(self.on_progress_changed)
        self.thread.finished.connect(self.show_plot)
        self.thread.start()
        print("thread init")

    def show_plot(self):
        self.thread = None
        graphs.show_plot(self.hiv_checkbox.isChecked(),
                         self.sti_checkbox.isChecked(),
                         self.extshift_checkbox.isChecked(),
                         self.color_combo1.currentText(),
                         self.style_combo1.currentText(),
                         self.color_combo2.currentText(),
                         self.style_combo2.currentText(),
                         self.color_combo3.currentText(),
                         self.style_combo3.currentText())

    def on_progress_changed(self, method_name, value):
        self.progresslabel.setText(method_name)
        self.progressbar.setValue(value)

    # Проверка на корректность ввода для u1 и u2 и обновления setting
    def check_input_float(self, line_edit, original_text_key):
        text = line_edit.text()

        pattern = r"^(0|[1-9]\d*)(\.\d*[1-9])?$"
        match = re.match(pattern, text)
        if match:
            self.setting[original_text_key] = line_edit.text()
            self.save_setting()
        else:
            line_edit.setText(self.setting[original_text_key])

    # Обновление setting
    def update_setting(self, key, value):
        self.setting[key] = value
        self.save_setting()

    # Сохранение нового setting
    def save_setting(self):
        with open('setting.gui', 'wb') as p:
            pickle.dump(self.setting, p)


if __name__ == '__main__':
    import sys
    import os

    if not os.path.isfile('setting.gui'):
        with open('setting.gui', 'wb') as p:
            pickle.dump(
                {"u1": "0.7", "u2": "0.3", "tf": "1000", "s": "5", "l": "20",
                 "hiv": ("green", "dashed"),
                 "sti": ("red", "dotted"),
                 "extshift": ("blue", "solid")}, p)

    with open('setting.gui', 'rb') as f:
        setting = pickle.load(f)

    app = QApplication(sys.argv)
    win = MainWindow(setting)
    win.show()
    app.exec_()
