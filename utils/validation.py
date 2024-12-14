from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

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
        validator = QIntValidator()  # Разрешает только целые числа, включая отрицательные
        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        # Устанавливаем текст редактора на основе значения ячейки
        value = index.model().data(index, Qt.EditRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        # Сохраняем введенное значение в модель
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def apply_to_line_edit(self, line_edit):
        """
        Применяет валидатор для QLineEdit.
        """
        validator = QIntValidator()  # Валидатор для целых чисел
        line_edit.setValidator(validator)

def validate_table(table, table_name):
    """
    Проверяет таблицу на наличие пустых ячеек.

    :param table: QTableWidget, таблица для проверки
    :param table_name: str, название таблицы для сообщения об ошибке
    :return: bool, True если ошибок нет, иначе False
    """
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
    """
    Проверяет, задана ли хотя бы одна опора.
    :param left_support: Состояние левой опоры (bool)
    :param right_support: Состояние правой опоры (bool)
    :return: True, если хотя бы одна опора задана; False, иначе.
    """
    return left_support or right_support


def validate_table_row_counts(nodes_table, rods_table):
    """
    Проверяет, что в таблице узлов не менее двух строк и в таблице стержней не менее одной строки.
    :param nodes_table: Таблица узлов (QTableWidget)
    :param rods_table: Таблица стержней (QTableWidget)
    :return: True, если условия выполнены; False, иначе.
    """
    nodes_count = nodes_table.rowCount()
    rods_count = rods_table.rowCount()

    if nodes_count < 2:
        return False, "Таблица узлов должна содержать не менее двух строк."
    if rods_count < 1:
        return False, "Таблица стержней должна содержать не менее одной строки."

    return True, ""


def validate_node_order(nodes_table):
    """
    Проверяет, что значения в таблице узлов упорядочены по возрастанию.
    Первое значение всегда должно быть равно "0".
    :param nodes_table: Таблица узлов (QTableWidget)
    :return: True, если условия выполнены; False и сообщение об ошибке, если нет.
    """
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
    """
    Проверяет, что все значения узлов >= 0.
    :param nodes_table: Таблица узлов (QTableWidget)
    :return: True, если все значения >= 0; False и сообщение об ошибке, если нет.
    """
    try:
        for row in range(nodes_table.rowCount()):
            value = float(nodes_table.item(row, 0).text())
            if value < 0:
                return False, f"Значение в строке {row + 1} таблицы узлов должно быть >= 0."
    except (ValueError, AttributeError):
        return False, "Все значения в таблице узлов должны быть числовыми."
    return True, ""


def validate_node_and_rod_counts(nodes_table, rods_table):
    """
    Проверяет, что количество узлов на 1 больше, чем количество стержней.
    :param nodes_table: Таблица узлов (QTableWidget)
    :param rods_table: Таблица стержней (QTableWidget)
    :return: True, если количество узлов на 1 больше, чем стержней; False и сообщение об ошибке, если нет.
    """
    node_count = nodes_table.rowCount()
    rod_count = rods_table.rowCount()
    if node_count != rod_count + 1:
        return False, f"Количество узлов ({node_count}) должно быть на 1 больше, чем количество стержней ({rod_count})."
    return True, ""

def validate_node_lengths(nodes_table, rods_table):
    """
    Проверяет, что координата узла (k+1) больше координаты узла k
    на значение длины стержня с индексом k.
    :param nodes_table: Таблица узлов (QTableWidget)
    :param rods_table: Таблица стержней (QTableWidget)
    :return: True, если проверка пройдена; False и сообщение об ошибке, если нет.
    """
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
