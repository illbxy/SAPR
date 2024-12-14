from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit, QMessageBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, QLocale


class NumericDelegate(QStyledItemDelegate):
    """
    Делегат для проверки вводимых значений в ячейках таблицы и QLineEdit.
    Позволяет вводить только цифры и символ "-".
    """
    def createEditor(self, parent, option, index):
        # Создаем редактор QLineEdit с валидатором для таблицы
        return self._create_editor(parent)

    def _create_editor(self, parent):
        # Метод для создания QLineEdit с валидатором
        editor = QLineEdit(parent)
        validator = QDoubleValidator()  # Разрешает ввод чисел с плавающей точкой
        validator.setNotation(QDoubleValidator.StandardNotation)  # Только стандартное представление
        validator.setLocale(QLocale(QLocale.English))  # Устанавливаем английскую локаль
        editor.setValidator(validator)
        editor.installEventFilter(self)  # Устанавливаем фильтр событий для редактора
        return editor

    # def _create_editor(self, parent):
    #     # Метод для создания QLineEdit с валидатором
    #     editor = QLineEdit(parent)
    #     validator = QDoubleValidator()  # Разрешает только целые числа, включая отрицательные
    #     editor.setValidator(validator)
    #     return editor

    def setEditorData(self, editor, index):
        # Устанавливаем текст редактора на основе значения ячейки
        value = index.model().data(index, Qt.EditRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        # Сохраняем введенное значение в модель
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def eventFilter(self, obj, event):
        """
        Фильтр событий для разрешения только точки в качестве разделителя дробной части.
        """
        if isinstance(obj, QLineEdit) and event.type() == event.KeyPress:
            if event.text() == ',':
                return True  # Игнорируем запятую
        return super().eventFilter(obj, event)

    def apply_to_line_edit(self, line_edit):
        """
        Применяет валидатор для QLineEdit, позволяя вводить числа с точкой.
        """
        validator = QDoubleValidator()  # Валидатор для чисел с плавающей точкой
        validator.setNotation(QDoubleValidator.StandardNotation)  # Только стандартное представление
        validator.setLocale(QLocale(QLocale.English))  # Устанавливаем английскую локаль
        line_edit.setValidator(validator)
        line_edit.installEventFilter(self)  # Устанавливаем фильтр событий


def validate_table(table, table_name):

    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if not item or item.text().strip() == "":
                QMessageBox.warning(
                    None,
                    "Ошибка",
                    f"В таблице '{table_name}' есть пустые ячейки. "
                    f"Заполните все ячейки перед выполнением операции.",
                )
                return False
    return True

def validate_supports(left_support, right_support):

    return left_support or right_support


def validate_table_row_counts(nodes_table, rods_table):

    nodes_count = nodes_table.rowCount()
    rods_count = rods_table.rowCount()

    if nodes_count < 2:
        return False, "Таблица узлов должна содержать не менее двух строк."
    if rods_count < 1:
        return False, "Таблица стержней должна содержать не менее одной строки."

    return True, ""


def validate_node_order(nodes_table):

    row_count = nodes_table.rowCount()
    if row_count == 0:
        return False, "Таблица узлов не должна быть пустой."

    try:
        previous_value = float(nodes_table.item(0, 0).text())
        if previous_value != 0:
            return False, "Первое значение в таблице узлов должно быть равно '0'."

        for row in range(1, row_count):
            current_value = float(nodes_table.item(row, 0).text())
            if current_value <= previous_value:
                return False, f"Значение в строке {row + 1} должно быть больше значения в предыдущей строке."
            previous_value = current_value
    except (ValueError, AttributeError):
        return False, "Все значения в таблице узлов должны быть числовыми."

    return True, ""

def validate_node_values(nodes_table):

    try:
        for row in range(nodes_table.rowCount()):
            value = float(nodes_table.item(row, 0).text())
            if value < 0:
                return False, f"Значение в строке {row + 1} таблицы узлов должно быть >= 0."
    except (ValueError, AttributeError):
        return False, "Все значения в таблице узлов должны быть числовыми."
    return True, ""


def validate_node_and_rod_counts(nodes_table, rods_table):

    node_count = nodes_table.rowCount()
    rod_count = rods_table.rowCount()
    if node_count != rod_count + 1:
        return False, f"Количество узлов ({node_count}) должно быть на 1 больше, чем количество стержней ({rod_count})."
    return True, ""

def validate_node_lengths(nodes_table, rods_table):

    try:
        for k in range(rods_table.rowCount()):
            node_k = float(nodes_table.item(k, 0).text())
            node_k1 = float(nodes_table.item(k + 1, 0).text())
            rod_length = float(rods_table.item(k, 0).text())  # Предполагается, что длина стержня в первом столбце

            if not (node_k1 - node_k == rod_length):
                return False, (
                    f"Координата узла {k + 2} должна быть равна координате узла {k + 1} "
                    f"плюс длина стержня {k + 1} ({rod_length})."
                )
    except (ValueError, AttributeError) as e:
        return False, f"Ошибка проверки узлов и стержней: {e}"

    return True, ""
