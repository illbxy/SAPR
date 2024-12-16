# main_window.py
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QGraphicsView, QSplitter, QLabel, QFrame, QComboBox,
                             QDialogButtonBox, QDialog,
                             QMessageBox, QCheckBox, QLineEdit, QFileDialog, QGraphicsScene, QStackedWidget
                             )
from PyQt5.QtCore import Qt, pyqtSignal

from utils.validation import NumericDelegate, validate_table, validate_supports, validate_table_row_counts, \
    validate_node_order, validate_node_values, validate_node_and_rod_counts, validate_node_lengths, \
    validate_all_with_loads

from utils.file_handler import save_data, load_data
from models.node import Node
from models.rod import Rod
from models.load import Load

from gui.visualizer import plot_structure
from gui.postprocessor import Postprocessor

class ScalableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing, True)  # Устанавливаем антиалиасинг
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # Масштабирование под указателем мыши
        self.zoom_factor = 1.15  # Коэффициент масштабирования

    def wheelEvent(self, event):
        """
        Переопределяем событие колеса мыши для масштабирования.
        """
        if event.angleDelta().y() > 0:  # Прокрутка вверх
            self.scale(self.zoom_factor, self.zoom_factor)
        else:  # Прокрутка вниз
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

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
    clicked_to_postprocessor = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.nodes_table = None
        self.rods_table = None
        self.loads_table = None

        self.setWindowTitle("SAPR")
        self.resize(800, 600)
        self.stackedWidget = QStackedWidget(self)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.stackedWidget)

        self.postprocessor = Postprocessor()
        self.postprocessor.clicked_to_preprocessor.connect(self.to_preprocessor)
        self.stackedWidget.addWidget(self.postprocessor)

        self.setup_ui()
        self.stackedWidget.addWidget(self.central_widget)
        self.stackedWidget.setCurrentWidget(self.central_widget)

    def to_preprocessor(self):
        self.stackedWidget.setCurrentWidget(self.central_widget)

    def table_to_array(self, table_widget):
        rows = table_widget.rowCount()  # Количество строк
        cols = table_widget.columnCount()  # Количество столбцов
        data = []

        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = table_widget.item(row, col)
                # Проверяем, есть ли содержимое в ячейке
                row_data.append(item.text() if item else "")
            data.append(row_data)

        return data

    def table_to_array2(self, table_widget):
        rows = table_widget.rowCount()  # Количество строк
        cols = table_widget.columnCount()  # Количество столбцов
        data = []

        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = table_widget.item(row, col)

            data.append(float(item.text()) if item else float(""))

        return data

    def setup_ui(self):
        # Главный макет
        main_layout = QVBoxLayout(self.central_widget)

        main_label = QLabel("Препроцессор")

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
        self.loads_table = QTableWidget(0, 4)
        self.loads_table.setHorizontalHeaderLabels(["Тип", "F", "Стержень", "Узел"])
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
        clear_tables_button = QPushButton("Очистить таблицы")
        visualize_button = QPushButton("Визуализировать")
        to_postprocessor_button = QPushButton("Постпроцессор")
        to_postprocessor_button.clicked.connect(self.to_postprocessor)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(load_button)
        buttons_layout.addWidget(visualize_button)
        buttons_layout.addWidget(clear_tables_button)  # Добавляем в соответствующий layout

        left_panel.addLayout(buttons_layout)

        # Правая часть: окно для визуализации
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        splitter.addWidget(left_widget)

        # Создаём ScalableGraphicsView для визуализации
        self.graphics_view = ScalableGraphicsView()
        self.graphics_view.setFrameShape(QFrame.StyledPanel)

        # Инициализируем графическую сцену и связываем её с QGraphicsView
        self.scene = QGraphicsScene(self)  # Создаём графическую сцену
        self.graphics_view.setScene(self.scene)  # Связываем сцену с QGraphicsView

        splitter.addWidget(self.graphics_view)

        # Устанавливаем фиксированную ширину для таблиц (ширина таблицы "Стержни")
        left_widget.setFixedWidth(544)  # Устанавливаем фиксированную ширину

        splitter.setStretchFactor(0, 0)  # Левый панельный макет с таблицами (фиксированная ширина)
        splitter.setStretchFactor(1, 1)  # Визуализация будет растягиваться

        main_layout.addWidget(main_label)
        main_layout.addWidget(splitter)
        main_layout.addWidget(to_postprocessor_button)

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
        clear_tables_button.clicked.connect(self.clear_all_tables)

        # Связь кнопки с визуализацией
        visualize_button.clicked.connect(self.plot_structure)

        # Подключаем делегат ко всем таблицам
        numeric_delegate = NumericDelegate()
        self.nodes_table.setItemDelegate(numeric_delegate)
        self.rods_table.setItemDelegate(numeric_delegate)
        self.loads_table.setItemDelegate(numeric_delegate)

        self.delegate = NumericDelegate()
        self.delegate.apply_to_line_edit(self.e_input)

    def to_postprocessor(self):

        # Пример вызова функции
        is_valid, message = validate_all_with_loads(self.nodes_table, self.rods_table, self.loads_table)
        if not is_valid:
            QMessageBox.warning(None, "Ошибка", message)
            return


        self.postprocessor.set_array(self.table_to_array2(self.nodes_table), self.table_to_array(self.rods_table), self.table_to_array(self.loads_table), self.check_left_support.isChecked(), self.check_right_support.isChecked())
        self.postprocessor.create_matrix_A()
        self.postprocessor.defenition()
        self.postprocessor.create_matrix_B()
        self.postprocessor.create_delta_x()
        self.postprocessor.fill_table()
        self.stackedWidget.setCurrentWidget(self.postprocessor)

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

                # Устанавливаем прочерк в зависимости от типа нагрузки
                if load_type == "Сосредоточенная":
                    self.loads_table.setItem(row_count, 2, QTableWidgetItem("-"))  # Стержень
                    self.loads_table.setItem(row_count, 3, QTableWidgetItem(""))  # Узел (заполняемый)
                elif load_type == "Продольная":
                    self.loads_table.setItem(row_count, 2, QTableWidgetItem(""))  # Стержень (заполняемый)
                    self.loads_table.setItem(row_count, 3, QTableWidgetItem("-"))  # Узел

                # Блокируем редактирование в зависимости от типа нагрузки
                if load_type == "Сосредоточенная":
                    self.loads_table.item(row_count, 2).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Стержень
                elif load_type == "Продольная":
                    self.loads_table.item(row_count, 3).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Узел

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

        # Пример вызова функции
        is_valid, message = validate_all_with_loads(self.nodes_table, self.rods_table, self.loads_table)
        if not is_valid:
            QMessageBox.warning(None, "Ошибка", message)
            return


        """
        Сохраняет данные из таблиц в файл через file_handler.
        """

        # Проверка длины стержней
        is_valid, error_message = validate_node_lengths(self.nodes_table, self.rods_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка положительности значений узлов
        is_valid, error_message = validate_node_values(self.nodes_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка соответствия количества узлов и стержней
        is_valid, error_message = validate_node_and_rod_counts(self.nodes_table, self.rods_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка порядка значений в таблице узлов
        is_valid, error_message = validate_node_order(self.nodes_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка количества строк в таблицах
        is_valid, error_message = validate_table_row_counts(self.nodes_table, self.rods_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверяем наличие хотя бы одной опоры
        if not validate_supports(self.check_left_support.isChecked(), self.check_right_support.isChecked()):
            QMessageBox.warning(self, "Ошибка", "Должна быть задана хотя бы одна опора.")
            return

        # Проверяем таблицы перед сохранением
        if not validate_table(self.nodes_table, "Узлы") or \
                not validate_table(self.rods_table, "Стержни") or \
                not validate_table(self.loads_table, "Нагрузки"):
            return  # Прекращаем выполнение, если есть ошибки

        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "JSON Files (*.json)")
        if file_name:
            #Логика сохранения
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
                    self.loads_table.item(row, 3).text(),
                )
                for row in range(self.loads_table.rowCount())
            ]

            # Получение данных об опорах и модуле упругости
            supports = {
                "left": self.check_left_support.isChecked(),
                "right": self.check_right_support.isChecked(),
            }
            modulus_of_elasticity = self.e_input.text()

            save_data(file_name, nodes, rods, loads, supports, modulus_of_elasticity)

    def load_file(self):
        """
        Загружает данные из файла через file_handler.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "", "JSON Files (*.json)")
        if file_name:
            try:
                nodes, rods, loads, supports, modulus_of_elasticity = load_data(file_name)

                # Обновляем таблицы
                self.set_table_data(self.nodes_table, [[node.x] for node in nodes])
                self.set_table_data(
                    self.rods_table,
                    [[rod.length, rod.area, rod.modulus, rod.stress] for rod in rods]
                )
                self.set_table_data(
                    self.loads_table,
                    [[load.load_type, load.force, load.rod, load.node] for load in loads]
                )

                # Обновляем опоры и модуль упругости
                self.check_left_support.setChecked(supports["left"])
                self.check_right_support.setChecked(supports["right"])
                self.e_input.setText(str(modulus_of_elasticity))

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

            # Визуализация при загрузке данных из файла
            self.plot_structure()

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

    def clear_all_tables(self):
        """
        Полностью очищает все таблицы.
        """
        # Очищаем таблицы
        self.nodes_table.setRowCount(0)
        self.rods_table.setRowCount(0)
        self.loads_table.setRowCount(0)

        # Устанавливаем пустое значение для модуля упругости
        self.e_input.clear()

        # Сбрасываем состояния опор
        self.check_left_support.setChecked(False)
        self.check_right_support.setChecked(False)

        QMessageBox.information(self, "Очистка", "Все данные успешно удалены.")

    def plot_structure(self):

        # Пример вызова функции
        is_valid, message = validate_all_with_loads(self.nodes_table, self.rods_table, self.loads_table)
        if not is_valid:
            QMessageBox.warning(None, "Ошибка", message)
            return


        """
        Собирает данные из таблиц и передает их в функцию визуализации.
        """
        # Проверка длины стержней
        is_valid, error_message = validate_node_lengths(self.nodes_table, self.rods_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка положительности значений узлов
        is_valid, error_message = validate_node_values(self.nodes_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка соответствия количества узлов и стержней
        is_valid, error_message = validate_node_and_rod_counts(self.nodes_table, self.rods_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка порядка значений в таблице узлов
        is_valid, error_message = validate_node_order(self.nodes_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверка количества строк в таблицах
        is_valid, error_message = validate_table_row_counts(self.nodes_table, self.rods_table)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        # Проверяем наличие хотя бы одной опоры
        if not validate_supports(self.check_left_support.isChecked(), self.check_right_support.isChecked()):
            QMessageBox.warning(self, "Ошибка", "Должна быть задана хотя бы одна опора.")
            return

        # Проверяем таблицы перед сохранением
        if not validate_table(self.nodes_table, "Узлы") or \
                not validate_table(self.rods_table, "Стержни") or \
                not validate_table(self.loads_table, "Нагрузки"):
            return  # Прекращаем выполнение, если есть ошибки

        # Считываем узлы
        nodes = []
        for row in range(self.nodes_table.rowCount()):
            try:
                x = float(self.nodes_table.item(row, 0).text())
                nodes.append(Node(x))
            except ValueError:
                QMessageBox.warning(self, "Ошибка", f"Некорректные данные в узле {row + 1}.")
                return

        # Считываем стержни
        rods = []
        for row in range(self.rods_table.rowCount()):
            try:
                length = float(self.rods_table.item(row, 0).text())
                area = float(self.rods_table.item(row, 1).text())
                modulus = float(self.rods_table.item(row, 2).text())
                stress = float(self.rods_table.item(row, 3).text())
                rods.append(Rod(length, area, modulus, stress))
            except ValueError:
                QMessageBox.warning(self, "Ошибка", f"Некорректные данные в стержне {row + 1}.")
                return

        # Считываем нагрузки
        loads = []
        for row in range(self.loads_table.rowCount()):
            try:
                load_type = self.loads_table.item(row, 0).text()
                force = float(self.loads_table.item(row, 1).text())
                rod = self.loads_table.item(row, 2).text() or "-"
                node = self.loads_table.item(row, 3).text() or "-"
                loads.append(Load(load_type, force, rod, node))
            except ValueError:
                QMessageBox.warning(self, "Ошибка", f"Некорректные данные в нагрузке {row + 1}.")
                return

        # Проверка опор для визуализации
        left_support = self.check_left_support.isChecked()
        right_support = self.check_right_support.isChecked()

        # Передача данных в функцию визуализации
        plot_structure(self.graphics_view.scene(), nodes, rods, loads, left_support, right_support)

