# main_window.py

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QGraphicsView, QSplitter, QLabel, QFrame, QComboBox,
                             QDialogButtonBox, QDialog,
                             QMessageBox, QCheckBox, QLineEdit, QFileDialog
                             )
from PyQt5.QtCore import Qt

from utils.validation import NumericDelegate

from utils.file_handler import save_data, load_data
from models.node import Node
from models.rod import Rod
from models.load import Load

# from visualizer import Visualizer


class LoadTypeDialog(QDialog):
    """
    Диалоговое окно для выбора типа нагрузки.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор типа нагрузки")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        # Основной макет
        layout = QVBoxLayout(self)

        # Выпадающий список
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Сосредоточенная", "Продольная"])
        layout.addWidget(QLabel("Выберите тип нагрузки:"))
        layout.addWidget(self.combo_box)

        # Кнопки OK и Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_selected_load_type(self):
        """
        Возвращает выбранный тип нагрузки.
        """
        return self.combo_box.currentText()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAPR")
        self.resize(800, 600)
        self.setup_ui()
        # self.setup_visualizer()

    def setup_ui(self):
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный макет
        main_layout = QVBoxLayout(central_widget)

        # Таблица "Узлы"
        nodes_label = QLabel("Узлы")
        self.nodes_table = QTableWidget(0, 1)
        self.nodes_table.setHorizontalHeaderLabels(["X"])
        nodes_add_button = QPushButton("Добавить строку")
        nodes_del_button = QPushButton("Удалить строку")
        nodes_button_layout = QHBoxLayout()
        nodes_button_layout.addWidget(nodes_add_button)
        nodes_button_layout.addWidget(nodes_del_button)

        # Чекбоксы
        self.check_left_support = QCheckBox("Левая опора")
        self.check_right_support = QCheckBox("Правая опора")
        self.check_left_support.setChecked(False)
        self.check_right_support.setChecked(False)

        # Левый панельный макет
        left_panel = QVBoxLayout()
        left_panel.addWidget(nodes_label)
        left_panel.addWidget(self.nodes_table)
        left_panel.addLayout(nodes_button_layout)

        # Модуль упругости E
        self.e_label = QLabel("Модуль упругости E:")
        self.e_input = QLineEdit()
        left_panel.addWidget(self.check_left_support)
        left_panel.addWidget(self.check_right_support)
        left_panel.addWidget(self.e_label)
        left_panel.addWidget(self.e_input)

        # Таблица "Стержни"
        rods_label = QLabel("Стержни")
        self.rods_table = QTableWidget(0, 4)
        self.rods_table.setHorizontalHeaderLabels(["L", "A", "E", "σ"])
        rods_add_button = QPushButton("Добавить строку")
        rods_del_button = QPushButton("Удалить строку")
        rods_button_layout = QHBoxLayout()
        rods_button_layout.addWidget(rods_add_button)
        rods_button_layout.addWidget(rods_del_button)

        left_panel.addWidget(rods_label)
        left_panel.addWidget(self.rods_table)
        left_panel.addLayout(rods_button_layout)

        # Таблица "Нагрузки"
        loads_label = QLabel("Нагрузки")
        self.loads_table = QTableWidget(0, 3)
        self.loads_table.setHorizontalHeaderLabels(["Тип", "F", "Направление"])
        loads_add_button = QPushButton("Добавить строку")
        loads_del_button = QPushButton("Удалить строку")
        loads_button_layout = QHBoxLayout()
        loads_button_layout.addWidget(loads_add_button)
        loads_button_layout.addWidget(loads_del_button)

        left_panel.addWidget(loads_label)
        left_panel.addWidget(self.loads_table)
        left_panel.addLayout(loads_button_layout)

        # Добавляем кнопки "Сохранить файл", "Загрузить файл", "Визуализировать"
        buttons_layout = QVBoxLayout()
        save_button = QPushButton("Сохранить файл")
        load_button = QPushButton("Загрузить файл")
        visualize_button = QPushButton("Визуализировать")

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(load_button)
        buttons_layout.addWidget(visualize_button)

        left_panel.addLayout(buttons_layout)

        # Правая часть: окно для визуализации
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        splitter.addWidget(left_widget)

        self.graphics_view = QGraphicsView()
        self.graphics_view.setFrameShape(QFrame.StyledPanel)
        splitter.addWidget(self.graphics_view)

        # Устанавливаем фиксированную ширину для таблиц (ширина таблицы "Стержни")
        left_widget.setFixedWidth(544)  # Устанавливаем фиксированную ширину

        splitter.setStretchFactor(0, 0)  # Левый панельный макет с таблицами (фиксированная ширина)
        splitter.setStretchFactor(1, 1)  # Визуализация будет растягиваться

        main_layout.addWidget(splitter)

        # Связываем кнопки с действиями
        nodes_add_button.clicked.connect(lambda: self.add_row(self.nodes_table))
        nodes_del_button.clicked.connect(lambda: self.remove_row(self.nodes_table))
        rods_add_button.clicked.connect(lambda: self.add_row(self.rods_table))
        rods_del_button.clicked.connect(lambda: self.remove_row(self.rods_table))
        loads_add_button.clicked.connect(lambda: self.add_row(self.loads_table))
        loads_del_button.clicked.connect(lambda: self.remove_row(self.loads_table))

        # Подключаем действия к кнопкам
        save_button.clicked.connect(self.save_file)
        load_button.clicked.connect(self.load_file)
        # visualize_button.clicked.connect(self.visualize)

        # Подключаем делегат ко всем таблицам
        numeric_delegate = NumericDelegate()
        self.nodes_table.setItemDelegate(numeric_delegate)
        self.rods_table.setItemDelegate(numeric_delegate)
        self.loads_table.setItemDelegate(numeric_delegate)

    def add_row(self, table):
        """
        Добавляет строку в таблицу.
        """
        row_count = table.rowCount()
        if table == self.rods_table:  # Если добавляется строка в таблицу "Стержни"
            e_value = self.e_input.text()
            if e_value:
                row_count = self.rods_table.rowCount()
                self.rods_table.insertRow(row_count)
                self.rods_table.setItem(row_count, 2, QTableWidgetItem(e_value))  # Установка модуля упругости в соответствующую колонку
            else:
                QMessageBox.information(self, "Ошибка", "Модуль упругости не задан")
        elif table == self.loads_table:
            dialog = LoadTypeDialog()
            if dialog.exec_() == QDialog.Accepted:  # Если нажата кнопка OK
                load_type = dialog.get_selected_load_type()
                row_count = self.loads_table.rowCount()
                self.loads_table.insertRow(row_count)
                self.loads_table.setItem(row_count, 0, QTableWidgetItem(load_type))
        else:
            table.insertRow(row_count)

    def remove_row(self, table):
        """
        Удаляет выбранную строку из таблицы.
        """
        current_row = table.currentRow()
        if current_row >= 0:  # Проверка, что строка выделена
            table.removeRow(current_row)

    def save_file(self):
        """
        Сохраняет данные из таблиц в файл через file_handler.
        """
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "JSON Files (*.json)")
        if file_name:
            nodes = [Node(self.nodes_table.item(row, 0).text()) for row in range(self.nodes_table.rowCount())]
            rods = [
                Rod(
                    self.rods_table.item(row, 0).text(),
                    self.rods_table.item(row, 1).text(),
                    self.rods_table.item(row, 2).text(),
                    self.rods_table.item(row, 3).text(),
                )
                for row in range(self.rods_table.rowCount())
            ]
            loads = [
                Load(
                    self.loads_table.item(row, 0).text(),
                    self.loads_table.item(row, 1).text(),
                    self.loads_table.item(row, 2).text(),
                )
                for row in range(self.loads_table.rowCount())
            ]
            save_data(file_name, nodes, rods, loads)

    def load_file(self):
        """
        Загружает данные из файла через file_handler.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "", "JSON Files (*.json)")
        if file_name:
            try:
                nodes, rods, loads = load_data(file_name)

                # Обновляем таблицы
                self.set_table_data(self.nodes_table, [[node.x] for node in nodes])
                self.set_table_data(
                    self.rods_table,
                    [[rod.length, rod.area, rod.modulus, rod.stress] for rod in rods]
                )
                self.set_table_data(
                    self.loads_table,
                    [[load.load_type, load.force, load.direction] for load in loads]
                )
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def set_table_data(self, table, data):
        """
        Заполняет таблицу данными.
        :param table: QTableWidget, который нужно заполнить
        :param data: Список списков, где каждый вложенный список соответствует строке таблицы
        """
        table.setRowCount(0)  # Очистка таблицы
        for row_data in data:
            if len(row_data) != table.columnCount():
                QMessageBox.warning(self, "Ошибка", "Некорректное количество столбцов в данных.")
                return
            row_count = table.rowCount()
            table.insertRow(row_count)
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row_count, col, item)


    # def setup_visualizer(self):
    #     """
    #     Инициализация визуализатора.
    #     """
    #     self.visualizer = Visualizer(self.graphics_view)
    #
    # def load_data(self, file_path):
    #     """
    #     Загружает данные из файла и вызывает визуализацию.
    #     """
    #     # Пример загрузки данных
    #     data = self.load_json(file_path)
    #     self.visualizer.visualize(data)
    #
    # def load_json(self, file_path):
    #     """
    #     Загружает данные из JSON-файла.
    #     """
    #     import json
    #     with open(file_path, 'r') as f:
    #         return json.load(f)
