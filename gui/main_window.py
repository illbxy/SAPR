from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QFileDialog, QSplitter, QLabel
)
from PyQt5.QtCore import Qt
from gui.visualizer import visualize_structure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Система автоматизации расчётов")
        self.setGeometry(100, 100, 1200, 800)  # Увеличим размер окна

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Левый виджет: Таблицы данных
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        main_layout.addWidget(left_widget)

        # Таблица узлов
        self.node_table = QTableWidget(0, 2)
        self.node_table.setHorizontalHeaderLabels(["X", "Y"])
        left_layout.addWidget(QLabel("Узлы"))
        left_layout.addWidget(self.node_table)
        self.add_node_button = QPushButton("Добавить узел")
        self.add_node_button.clicked.connect(self.add_node)
        left_layout.addWidget(self.add_node_button)

        # Таблица стержней
        self.element_table = QTableWidget(self)
        self.element_table.setColumnCount(6)  # Увеличиваем количество столбцов до 6
        self.element_table.setHorizontalHeaderLabels([
            "Начальный узел",  # Узел, с которого начинается стержень
            "Конечный узел",  # Узел, на котором заканчивается стержень
            "Длина L",  # Длина стержня
            "Площадь A",  # Площадь поперечного сечения
            "Модуль упругости E",  # Модуль упругости материала
            "Допускаемое напряжение [σ]"  # Допустимое напряжение
        ])
        self.element_table.setRowCount(0)  # Начинаем с пустой таблицы
        left_layout.addWidget(QLabel("Стержни"))
        left_layout.addWidget(self.element_table)
        self.add_element_button = QPushButton("Добавить стержень")
        self.add_element_button.clicked.connect(self.add_element)
        left_layout.addWidget(self.add_element_button)

        # Таблица нагрузок
        self.force_table = QTableWidget(0, 2)
        self.force_table.setHorizontalHeaderLabels(["Узел", "Сила"])
        left_layout.addWidget(QLabel("Нагрузки"))
        left_layout.addWidget(self.force_table)
        self.add_force_button = QPushButton("Добавить нагрузку")
        self.add_force_button.clicked.connect(self.add_force)
        left_layout.addWidget(self.add_force_button)

        # Кнопки сохранения и визуализации
        self.visualize_button = QPushButton("Визуализировать")
        self.visualize_button.clicked.connect(self.update_visualization)
        left_layout.addWidget(self.visualize_button)

        self.save_button = QPushButton("Сохранить проект")
        self.save_button.clicked.connect(self.save_project)
        left_layout.addWidget(self.save_button)

        # Правый виджет: Визуализация
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Данные
        self.nodes = []  # Список узлов
        self.elements = []  # Список стержней
        self.forces = []  # Список нагрузок

    def add_node(self):
        """
        Добавляет узел в таблицу и обновляет данные.
        """
        self.node_table.insertRow(self.node_table.rowCount())
        self.nodes.append((0, 0))  # Добавляем узел по умолчанию
        self.update_visualization()

    def add_element(self):
        """
        Добавляет стержень в таблицу и обновляет данные.
        """
        self.element_table.insertRow(self.element_table.rowCount())
        self.elements.append((0, 0))  # Добавляем стержень по умолчанию
        self.update_visualization()

    def add_force(self):
        """
        Добавляет нагрузку в таблицу и обновляет данные.
        """
        self.force_table.insertRow(self.force_table.rowCount())
        self.forces.append((0, 0))  # Добавляем нагрузку по умолчанию
        self.update_visualization()

    def update_visualization(self):
        """
        Обновляет визуализацию конструкции с учетом прямоугольных стержней.
        """
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_title("Визуализация конструкции")
            ax.set_xlabel("Координата X")
            ax.set_ylabel("Координата Y")

            # Узлы
            self.nodes = []
            for row in range(self.node_table.rowCount()):
                x_item = self.node_table.item(row, 0)
                y_item = self.node_table.item(row, 1)
                if x_item and y_item:
                    x = float(x_item.text())
                    y = float(y_item.text())
                    self.nodes.append((x, y))
                else:
                    raise ValueError("Узел содержит некорректные данные.")

            # Стержни
            self.elements = []
            for row in range(self.element_table.rowCount()):
                start_item = self.element_table.item(row, 0)
                end_item = self.element_table.item(row, 1)
                length_item = self.element_table.item(row, 2)
                area_item = self.element_table.item(row, 3)

                if start_item and end_item and length_item and area_item:
                    start = int(start_item.text())
                    end = int(end_item.text())
                    length = float(length_item.text())
                    area = float(area_item.text())

                    if start < len(self.nodes) and end < len(self.nodes):
                        self.elements.append((start, end, length, area))
                    else:
                        raise ValueError("Стержень ссылается на несуществующий узел.")
                else:
                    raise ValueError("Стержень содержит некорректные данные.")

            # Нагрузки
            self.forces = []
            for row in range(self.force_table.rowCount()):
                node_item = self.force_table.item(row, 0)
                force_item = self.force_table.item(row, 1)
                if node_item and force_item:
                    node = int(node_item.text())
                    force = float(force_item.text())
                    if node < len(self.nodes):
                        self.forces.append((node, force))
                    else:
                        raise ValueError("Нагрузка ссылается на несуществующий узел.")
                else:
                    raise ValueError("Нагрузка содержит некорректные данные.")

            # Визуализация стержней как прямоугольников
            for start, end, length, area in self.elements:
                x_coords = [self.nodes[start][0], self.nodes[end][0]]
                y_coords = [self.nodes[start][1], self.nodes[end][1]]
                width = (area ** 0.5) * 0.1  # Масштабируем площадь в ширину
                ax.plot(x_coords, y_coords, 'b-', lw=width * 10)  # Рисуем с толщиной, зависящей от площади

            # Визуализация нагрузок
            for node_index, force_value in self.forces:
                x, y = self.nodes[node_index]
                direction = -0.5 if force_value < 0 else 0.5
                ax.arrow(x, y, 0, direction, head_width=0.2, head_length=0.2, fc='red', ec='red')
                ax.text(x, y + direction * 1.2, f"{force_value:.2f} Н", color='red', ha='center', fontsize=9)

            ax.grid(True)
            ax.axis('equal')
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка визуализации", f"Ошибка: {str(e)}")
    def save_project(self):
        """
        Сохраняет проект в файл JSON.
        """
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить проект", "", "JSON Files (*.json)")
        if filename:
            try:
                project_data = {
                    "nodes": self.nodes,
                    "elements": self.elements,
                    "forces": self.forces,
                }
                from utils.file_handler import save_project
                save_project(project_data, filename)
                QMessageBox.information(self, "Успех", f"Проект сохранён в {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении проекта: {str(e)}")
