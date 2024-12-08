from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, \
    QGraphicsView, QGraphicsScene, QComboBox, QLabel, QLineEdit, QFileDialog, QSizePolicy
from gui.visualizer import Visualizer
import math

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("Инициализация окна...")

        # Устанавливаем заголовок и размер окна
        self.setWindowTitle("SAPR - Препроцессор")
        self.setGeometry(100, 100, 1400, 800)

        try:
            # Инициализация таблицы узлов
            self.node_table = QTableWidget(self)
            self.node_table.setRowCount(0)
            self.node_table.setColumnCount(1)
            self.node_table.setHorizontalHeaderLabels(["Координаты"])

            # Поле для модуля упругости
            self.modulus_label = QLabel("Модуль упругости (общий):", self)
            self.modulus_input = QLineEdit(self)
            self.modulus_input.setText("200000")

            # Инициализация таблицы стержней
            self.element_table = QTableWidget(self)
            self.element_table.setRowCount(0)
            self.element_table.setColumnCount(3)
            self.element_table.setHorizontalHeaderLabels(["Длина", "Площадь", "Модуль упругости"])

            # Инициализация таблицы нагрузок
            self.load_table = QTableWidget(self)
            self.load_table.setRowCount(0)
            self.load_table.setColumnCount(4)
            self.load_table.setHorizontalHeaderLabels(["Тип нагрузки", "Сила", "1-й узел", "2-й узел"])

            # Кнопки для добавления элементов
            self.add_node_button = QPushButton("+ Узел", self)
            self.add_node_button.clicked.connect(self.add_node)

            self.add_element_button = QPushButton("+ Стержень", self)
            self.add_element_button.clicked.connect(self.add_element)

            self.add_load_button = QPushButton("+ Нагрузка", self)
            self.add_load_button.clicked.connect(self.add_load)

            # Кнопки для удаления элементов
            self.delete_node_button = QPushButton("- Узел", self)
            self.delete_node_button.clicked.connect(self.delete_node)

            self.delete_element_button = QPushButton("- Стержень", self)
            self.delete_element_button.clicked.connect(self.delete_element)

            self.delete_load_button = QPushButton("- Нагрузка", self)
            self.delete_load_button.clicked.connect(self.delete_load)

            # Комбо-бокс для выбора типа нагрузки
            self.load_type_combo = QComboBox(self)
            self.load_type_combo.addItem("Сосредоточенная")
            self.load_type_combo.addItem("Продольная")

            # Кнопки для сохранения и загрузки данных
            self.save_button = QPushButton("Сохранить в файл", self)
            self.save_button.clicked.connect(self.save_to_file)

            self.load_button = QPushButton("Загрузить из файла", self)
            self.load_button.clicked.connect(self.load_from_file)

            # Инициализация визуализатора
            self.visualizer = Visualizer(self)

            # Кнопка для визуализации
            self.visualize_button = QPushButton("Визуализировать", self)
            self.visualize_button.clicked.connect(self.visualize)

            # Инициализация области для визуализации конструкции
            self.graphics_view = QGraphicsView(self)
            self.scene = QGraphicsScene(self)
            self.graphics_view.setScene(self.scene)
            self.graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Расположение элементов в макете
            main_layout = QHBoxLayout()
            left_layout = QVBoxLayout()

            # Добавляем таблицы и кнопки в левую часть
            left_layout.addWidget(self.node_table)
            left_layout.addWidget(self.add_node_button)
            left_layout.addWidget(self.delete_node_button)
            left_layout.addWidget(self.modulus_label)
            left_layout.addWidget(self.modulus_input)
            left_layout.addWidget(self.element_table)
            left_layout.addWidget(self.add_element_button)
            left_layout.addWidget(self.delete_element_button)
            left_layout.addWidget(self.load_table)
            left_layout.addWidget(self.add_load_button)
            left_layout.addWidget(self.delete_load_button)
            left_layout.addWidget(self.load_type_combo)
            left_layout.addWidget(self.save_button)
            left_layout.addWidget(self.load_button)
            left_layout.addWidget(self.visualize_button)  # Кнопка визуализации

            main_layout.addLayout(left_layout)

            # Добавляем область визуализации в правую часть
            main_layout.addWidget(self.graphics_view)

            # Устанавливаем центральный виджет
            central_widget = QWidget(self)
            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Сигналы для масштабирования
            self.scale_factor = 1.0  # Начальный масштаб
            self.setMouseTracking(True)

            print("Инициализация завершена.")

        except Exception as e:
            print(f"Ошибка при инициализации окна: {e}")
            return

    def wheelEvent(self, event):
        """Обрабатываем события колесика мыши для масштабирования"""
        zoom_in_factor = 1.2
        zoom_out_factor = 0.8
        if event.angleDelta().y() > 0:
            self.scale_view(zoom_in_factor)
        else:
            self.scale_view(zoom_out_factor)

    def scale_view(self, factor):
        """Масштабируем область визуализации"""
        self.scale_factor *= factor
        self.graphics_view.setTransform(self.graphics_view.transform().scale(factor, factor))

    def visualize(self):
        try:
            # Очищаем старую визуализацию
            self.scene.clear()

            # Получаем данные о узлах
            nodes = []
            for row in range(self.node_table.rowCount()):
                coord = self.node_table.item(row, 0).text()
                nodes.append([float(coord) * 100, 0])  # Масштабируем координаты узлов на 100

            # Получаем данные о стержнях
            elements = []
            for row in range(self.element_table.rowCount()):
                length = float(self.element_table.item(row, 0).text()) * 100  # Масштабируем длину стержня на 100
                area = float(self.element_table.item(row, 1).text())
                modulus = float(self.element_table.item(row, 2).text())
                elements.append((length, area, modulus))

            # Рисуем только узлы по боковым сторонам стержней
            for i, (x, y) in enumerate(nodes):
                radius = 5  # Размер узла
                self.scene.addEllipse(x - radius, y - radius, 2 * radius, 2 * radius, QPen(Qt.red), Qt.red)

            # Рисуем стержни как прямоугольники
            for i in range(len(nodes) - 1):
                (x1, y1) = nodes[i]
                (x2, y2) = nodes[i + 1]

                # Получаем длину стержня и его площадь
                length = elements[i][0]
                area = elements[i][1]

                # Высота стержня (квадратный корень из площади)
                height = math.sqrt(area) * 100  # Масштабируем высоту на 100
                width = 50  # Масштабируем ширину на 50

                # Расположение стержня по оси OX
                rect_x = min(x1, x2)  # Левый край прямоугольника
                rect_y = min(y1, y2)  # Верхний край прямоугольника

                # Рисуем прямоугольник для стержня (на оси OX)
                pen = QPen(Qt.black)
                pen.setWidth(2)
                self.scene.addRect(rect_x, rect_y - height / 2, length, height, pen)  # Стержень уходит вверх и вниз

                # Узлы по боковым сторонам стержня
                mid_y_top = y1 - height / 2  # Верхний узел
                mid_y_bottom = y1 + height / 2  # Нижний узел

                # Узлы на боковых сторонах
                node1_x, node1_y = x1, mid_y_top  # Верхний узел на левой стороне
                node2_x, node2_y = x2, mid_y_top  # Верхний узел на правой стороне

                node3_x, node3_y = x1, mid_y_bottom  # Нижний узел на левой стороне
                node4_x, node4_y = x2, mid_y_bottom  # Нижний узел на правой стороне

                # Рисуем узлы (красные точки) по боковым сторонам стержня
                radius = 5  # Размер узла
                self.scene.addEllipse(node1_x - radius, node1_y - radius, 2 * radius, 2 * radius, QPen(Qt.red), Qt.red)
                self.scene.addEllipse(node2_x - radius, node2_y - radius, 2 * radius, 2 * radius, QPen(Qt.red), Qt.red)
                self.scene.addEllipse(node3_x - radius, node3_y - radius, 2 * radius, 2 * radius, QPen(Qt.red), Qt.red)
                self.scene.addEllipse(node4_x - radius, node4_y - radius, 2 * radius, 2 * radius, QPen(Qt.red), Qt.red)

        except Exception as e:
            print(f"Ошибка при визуализации: {e}")
    def add_node(self):
        try:
            current_row_count = self.node_table.rowCount()
            self.node_table.insertRow(current_row_count)
            self.node_table.setItem(current_row_count, 0, QTableWidgetItem("0"))  # Координаты
            print(f"Добавлен узел: строка {current_row_count}")
        except Exception as e:
            print(f"Ошибка при добавлении узла: {e}")

    def add_element(self):
        try:
            current_row_count = self.element_table.rowCount()
            self.element_table.insertRow(current_row_count)

            # Заполняем длину и площадь значениями 0
            self.element_table.setItem(current_row_count, 0, QTableWidgetItem("0"))  # Длина
            self.element_table.setItem(current_row_count, 1, QTableWidgetItem("0"))  # Площадь

            # Используем общий модуль упругости
            modulus_value = self.modulus_input.text().strip()
            if not modulus_value:
                print("Ошибка: Модуль упругости не задан.")
                return

            self.element_table.setItem(current_row_count, 2, QTableWidgetItem(modulus_value))
            print(f"Добавлен стержень: строка {current_row_count}, модуль упругости: {modulus_value}")
        except Exception as e:
            print(f"Ошибка при добавлении стержня: {e}")

    def add_load(self):
        try:
            load_type = self.load_type_combo.currentText()  # Получаем выбранный тип нагрузки
            load_value = "100"  # По умолчанию значение нагрузки

            current_row_count = self.load_table.rowCount()
            self.load_table.insertRow(current_row_count)

            # Добавляем ячейки для типа, силы и узлов
            self.load_table.setItem(current_row_count, 0, QTableWidgetItem(load_type))
            self.load_table.setItem(current_row_count, 1, QTableWidgetItem(load_value))

            # Для сосредоточенной нагрузки второй узел всегда будет равен 0
            if load_type == "Сосредоточенная":
                self.load_table.setItem(current_row_count, 2, QTableWidgetItem("1"))  # 1-й узел
                self.load_table.setItem(current_row_count, 3, QTableWidgetItem("0"))  # 2-й узел

                # Устанавливаем второй узел как нередактируемый
                item = QTableWidgetItem("0")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                self.load_table.setItem(current_row_count, 3, item)
            elif load_type == "Продольная":
                self.load_table.setItem(current_row_count, 2, QTableWidgetItem("1"))  # 1-й узел
                self.load_table.setItem(current_row_count, 3, QTableWidgetItem("2"))  # 2-й узел

            print(f"Добавлена нагрузка: {load_type}, {load_value}")
        except Exception as e:
            print(f"Ошибка при добавлении нагрузки: {e}")

    def delete_node(self):
        try:
            current_row = self.node_table.currentRow()
            if current_row != -1:  # Если выбран элемент для удаления
                self.node_table.removeRow(current_row)
                print(f"Удален узел: {current_row}")
            else:
                print("Ошибка: Узел не выбран для удаления!")
        except Exception as e:
            print(f"Ошибка при удалении узла: {e}")

    def delete_element(self):
        try:
            current_row = self.element_table.currentRow()
            if current_row != -1:  # Если выбран элемент для удаления
                self.element_table.removeRow(current_row)
                print(f"Удален стержень: {current_row}")
            else:
                print("Ошибка: Стержень не выбран для удаления!")
        except Exception as e:
            print(f"Ошибка при удалении стержня: {e}")

    def delete_load(self):
        try:
            current_row = self.load_table.currentRow()
            if current_row != -1:  # Если выбран элемент для удаления
                self.load_table.removeRow(current_row)
                print(f"Удалена нагрузка: {current_row}")
            else:
                print("Ошибка: Нагрузка не выбрана для удаления!")
        except Exception as e:
            print(f"Ошибка при удалении нагрузки: {e}")

    def save_to_file(self):
        try:
            # Открываем диалог сохранения файла
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                       "JSON Files (*.json);;All Files (*)",
                                                       options=options)
            if not file_path:
                print("Сохранение отменено.")
                return

            # Сохраняем данные всех таблиц в словарь
            data = {
                "nodes": [[self.node_table.item(row, col).text() if self.node_table.item(row, col) else ""
                           for col in range(self.node_table.columnCount())]
                          for row in range(self.node_table.rowCount())],
                "elements": [[self.element_table.item(row, col).text() if self.element_table.item(row, col) else ""
                              for col in range(self.element_table.columnCount())]
                             for row in range(self.element_table.rowCount())],
                "loads": [[self.load_table.item(row, col).text() if self.load_table.item(row, col) else ""
                           for col in range(self.load_table.columnCount())]
                          for row in range(self.load_table.rowCount())],
            }

            # Запись данных в файл
            with open(file_path, "w", encoding="utf-8") as file:
                import json
                json.dump(data, file, indent=4, ensure_ascii=False)

            print(f"Данные успешно сохранены в '{file_path}'.")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def load_from_file(self):
        try:
            # Открываем диалог выбора файла
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                       "JSON Files (*.json);;All Files (*)",
                                                       options=options)
            if not file_path:
                print("Загрузка отменена.")
                return

            # Чтение данных из файла
            with open(file_path, "r", encoding="utf-8") as file:
                import json
                data = json.load(file)

            # Очистка и заполнение таблицы узлов
            self.node_table.setRowCount(0)
            for row_data in data.get("nodes", []):
                current_row = self.node_table.rowCount()
                self.node_table.insertRow(current_row)
                for col, value in enumerate(row_data):
                    self.node_table.setItem(current_row, col, QTableWidgetItem(value))

            # Очистка и заполнение таблицы стержней
            self.element_table.setRowCount(0)
            for row_data in data.get("elements", []):
                current_row = self.element_table.rowCount()
                self.element_table.insertRow(current_row)
                for col, value in enumerate(row_data):
                    self.element_table.setItem(current_row, col, QTableWidgetItem(value))

            # Очистка и заполнение таблицы нагрузок
            self.load_table.setRowCount(0)
            for row_data in data.get("loads", []):
                current_row = self.load_table.rowCount()
                self.load_table.insertRow(current_row)
                for col, value in enumerate(row_data):
                    self.load_table.setItem(current_row, col, QTableWidgetItem(value))

            print(f"Данные успешно загружены из '{file_path}'.")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
