import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, \
    QPushButton


class Postprocessor(QWidget):
    clicked_to_preprocessor = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.matrix_A = []
        self.array_B = []
        self.array_Delta = []
        self.nodes_array = []
        self.rods_array = []
        self.loads_array = []
        self.radspredelenni_array = []
        self.sosredotochni_array = []
        self.left_support = bool
        self.right_support = bool

        # Инициализация окна с таблицей
        self.setWindowTitle("Окно с таблицей")
        self.setGeometry(100, 100, 600, 400)

        # Добавляем кнопку "Назад"
        self.button_back = QPushButton("Препроцессор", self)
        self.button_back.clicked.connect(self.go_back)  # Подключаем обработчик клика


        # Главный вертикальный layout
        main_layout = QVBoxLayout(self)

        # Добавление метки
        label = QLabel("Постпроцессор")
        main_layout.addWidget(label)

        # Создание горизонтального layout для ввода и заголовков
        input_layout = QHBoxLayout()

        # Создание таблицы с 5 столбцами
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)  # Устанавливаем 6 столбцов
        self.table_widget.setRowCount(5)  # Устанавливаем 5 строк

        # Установка ширины второго столбца (нумерация начинается с 0)
        self.table_widget.setColumnWidth(5, 200)  # Установить ширину 150 пикселей для столбца с индексом 1

        # Устанавливаем заголовки столбцов
        self.table_widget.setHorizontalHeaderLabels(
            ["№ стержня", "x", "Nx", "σx", "Ux", "Допустимое напряжение"]
        )

        # Установка размеров таблицы (фиксированная ширина и высота)
        self.table_widget.setFixedWidth(850)  # Устанавливаем фиксированную ширину таблицы
        self.table_widget.setFixedHeight(500)  # Устанавливаем фиксированную высоту таблицы

        # Первый заголовок и строка для ввода
        label1 = QLabel("Шаг")
        self.input_line1 = QLineEdit(self)
        self.input_line1.setText("1")
        self.input_line1.editingFinished.connect(self.fill_table)
        self.input_line1.setPlaceholderText("Например: 0.25")

        # Второй заголовок и строка для ввода
        label2 = QLabel("Стержень")
        self.input_line2 = QLineEdit(self)
        self.input_line2.editingFinished.connect(self.fill_label_output)

        # self.input_line2.setPlaceholderText("Например: 4.2")

        label3 = QLabel("Локальная координата")
        self.input_line3 = QLineEdit(self)
        self.input_line3.editingFinished.connect(self.fill_label_output)

        self.label_output = QLabel("Nx: σx: Ux: ")

        # Добавляем заголовки и строки для ввода в горизонтальный layout
        input_layout.addWidget(label1)
        input_layout.addWidget(self.input_line1)
        input_layout.addWidget(label2)
        input_layout.addWidget(self.input_line2)
        input_layout.addWidget(label3)
        input_layout.addWidget(self.input_line3)

        # Добавление таблицы в layout
        main_layout.addWidget(self.table_widget)

        # Добавление горизонтального layout в основной вертикальный layout
        main_layout.addLayout(input_layout)

        main_layout.addWidget(self.label_output)

        # Добавление кнопки в layout
        main_layout.addWidget(self.button_back)

        # Установка layout для окна
        self.setLayout(main_layout)

    def set_array(self, nodes_array, rods_array, loads_array, left_support, right_support):
        self.nodes_array = nodes_array
        self.rods_array = rods_array
        self.loads_array = loads_array
        self.left_support = left_support
        self.right_support = right_support

        # print(self.nodes_array)
        # print(self.rods_array)
        # print(self.loads_array)

    def go_back(self):
        """Метод для возвращения в основное окно"""
        self.clicked_to_preprocessor.emit()  # Переключаем обратно на основное окно

    def create_matrix_A(self):
        self.matrix_A = [[0.0] * (len(self.nodes_array)) for _ in range(len(self.nodes_array))]

        for i in range(len(self.nodes_array) - 1):
            width = float(self.rods_array[i][0])
            height = float(self.rods_array[i][1])
            modulus_value = float(self.rods_array[i][2])


            if i == 0 and not self.left_support:
                self.matrix_A[i][i] = height / width * modulus_value
                self.matrix_A[i + 1][i] = -height / width * modulus_value
                self.matrix_A[i][i + 1] = -height / width * modulus_value
                if (len(self.nodes_array) - 1) == 1 and self.right_support:
                    self.matrix_A[i + 1][i + 1] = 1
                    self.matrix_A[i][i + 1] = 0
                    self.matrix_A[i + 1][i] = 0
                continue
            elif i == 0:
                self.matrix_A[i][i] = 1
                if (len(self.nodes_array) - 1) == 1 and self.left_support:
                    self.matrix_A[i + 1][i + 1] = height / width * modulus_value
                continue

            if i == (len(self.nodes_array) - 2) and not self.right_support:
                width2 = float(self.rods_array[i - 1][0])
                height2 = float(self.rods_array[i - 1][1])

                self.matrix_A[i][i] = (height2 / width2 * modulus_value) + (height / width * modulus_value)
                self.matrix_A[i + 1][i + 1] = height / width * modulus_value
                self.matrix_A[i][i + 1] = -height / width * modulus_value
                self.matrix_A[i + 1][i] = -height / width * modulus_value
                continue
            elif i == (len(self.nodes_array) - 2):
                width2 = float(self.rods_array[i - 1][0])
                height2 = float(self.rods_array[i - 1][1])

                self.matrix_A[i][i] = (height2 / width2 * modulus_value) + (height / width * modulus_value)
                self.matrix_A[i + 1][i + 1] = 1
                continue

            width2 = float(self.rods_array[i - 1][0])
            height2 = float(self.rods_array[i - 1][1])

            self.matrix_A[i][i] = (height / width * modulus_value) + (height2 / width2 * modulus_value)
            self.matrix_A[i + 1][i] = -height / width * modulus_value
            self.matrix_A[i][i + 1] = -height / width * modulus_value
        print(self.matrix_A)

    def create_matrix_B(self):
        self.array_B = [0.0] * (len(self.nodes_array))

        for i in range(len(self.nodes_array)):
            if i == 0 and self.left_support:
                continue
            if i == (len(self.nodes_array) - 1) and self.right_support:
                continue
            if i == 0:
                width = float(self.rods_array[i][0])
                radspredelenni_load = self.radspredelenni_array[i]
                sosredotochni_load = self.sosredotochni_array[i]

                self.array_B[i] = sosredotochni_load + radspredelenni_load * width / 2
            elif i == (len(self.nodes_array) - 1):
                width = float(self.rods_array[i - 1][0])
                radspredelenni_load = self.radspredelenni_array[i - 1]
                sosredotochni_load = self.sosredotochni_array[i]

                self.array_B[i] = sosredotochni_load + radspredelenni_load * width / 2
            else:
                width1 = float(self.rods_array[i - 1][0])
                width2 = float(self.rods_array[i][0])

                radspredelenni_load = self.radspredelenni_array[i - 1]
                radspredelenni_load2 = self.radspredelenni_array[i]

                sosredotochni_load = self.sosredotochni_array[i]

                self.array_B[i] = sosredotochni_load + radspredelenni_load * width1 / 2 + radspredelenni_load2 * width2 / 2
        print(self.array_B)

    def defenition(self):
        self.radspredelenni_array = [0.0] * (len(self.nodes_array) - 1)
        self.sosredotochni_array = [0.0] * (len(self.nodes_array))
        for i in range(len(self.loads_array)):
            if self.loads_array[i][0] == "Продольная":
                self.radspredelenni_array[int(self.loads_array[i][2]) - 1] = float(self.loads_array[i][1])

            if self.loads_array[i][0] == "Сосредоточенная":
                self.sosredotochni_array[int(self.loads_array[i][3]) - 1] = float(self.loads_array[i][1])
        print(self.radspredelenni_array)
        print(self.sosredotochni_array)

    def create_delta_x(self):
        self.array_Delta = np.linalg.solve(self.matrix_A, self.array_B).tolist()
        print(self.array_Delta)
    def calculation_ux_at_point(self, index, position):
        width = float(self.rods_array[index][0])
        height = float(self.rods_array[index][1])
        modulus_value = float(self.rods_array[index][2])

        radspredelenni_load = self.radspredelenni_array[index]


        return (self.array_Delta[index] + (position / width) * (self.array_Delta[index + 1] - self.array_Delta[index]) +
                (radspredelenni_load * width * position) / (2 * modulus_value * height) * (1 - position / width))

    def calculation_nx_at_point(self, index, position):
        width = float(self.rods_array[index][0])
        height = float(self.rods_array[index][1])
        modulus_value = float(self.rods_array[index][2])

        radspredelenni_load = self.radspredelenni_array[index]

        return (modulus_value * height / width * (self.array_Delta[index + 1] - self.array_Delta[index]) +
                radspredelenni_load * width * (1.0 - 2.0 * position / width) / 2.0)

    def calculation_sigmax_at_point(self, index, position):
        width = float(self.rods_array[index][0])
        height = float(self.rods_array[index][1])
        modulus_value = float(self.rods_array[index][2])

        radspredelenni_load = self.radspredelenni_array[index]

        nx = (modulus_value * height / width * (self.array_Delta[index + 1] - self.array_Delta[index]) +
              radspredelenni_load * width * (1.0 - 2.0 * position / width) / 2.0)

        return nx / height

    def fill_table(self):
        step = float(self.input_line1.text())
        self.table_widget.clearContents()

        total_rows = 0
        for rod in self.rods_array:
            width = float(rod[0])
            total_rows += int(width / step) + 1

        self.table_widget.setRowCount(total_rows)

        row = 0

        for index, rod in enumerate(self.rods_array):
            width = float(rod[0])
            position = 0.0

            while position <= width:
                ux = self.calculation_ux_at_point(index, position)
                nx = self.calculation_nx_at_point(index, position)
                sigmax = self.calculation_sigmax_at_point(index, position)

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(index + 1)))  # Номер стержня
                self.table_widget.setItem(row, 1, QTableWidgetItem(f"{position:.2f}"))  # Позиция x
                self.table_widget.setItem(row, 2, QTableWidgetItem(f"{nx:.2f}"))  # Nx
                self.table_widget.setItem(row, 3, QTableWidgetItem(f"{sigmax:.2f}"))  # σx
                self.table_widget.setItem(row, 4, QTableWidgetItem(f"{ux:.2f}"))  # Ux

                allowable_stress = float(self.rods_array[index][3])
                self.table_widget.setItem(row, 5, QTableWidgetItem(f"{allowable_stress:.2f}"))  # Допустимое напряжение

                # Переход к следующей позиции
                position += step
                row += 1
    def fill_label_output(self):
        if self.input_line2.text() and self.input_line3.text():
            self.label_output.setText(f"Nx: {self.calculation_nx_at_point(int(self.input_line2.text()) - 1, float(self.input_line3.text()))} "
                                      f"σx: {self.calculation_sigmax_at_point(int(self.input_line2.text()) - 1, float(self.input_line3.text()))}"
                                      f"Ux: {self.calculation_ux_at_point(int(self.input_line2.text()) - 1, float(self.input_line3.text()))}")