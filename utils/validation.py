from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class NumericDelegate(QStyledItemDelegate):
    """
    Делегат для проверки вводимых значений в ячейках таблицы.
    Позволяет вводить только цифры и символ "-".
    """
    def createEditor(self, parent, option, index):
        # Создаем редактор QLineEdit с валидатором
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
