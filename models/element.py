# models/element.py

class Element:
    def __init__(self, length, area, modulus, force=0):
        self.length = length      # Длина стержня
        self.area = area          # Площадь поперечного сечения
        self.modulus = modulus    # Модуль упругости
        self.force = force        # Сосредоточенная нагрузка на стержне (по умолчанию 0)

    def __str__(self):
        return f"Element(length={self.length}, area={self.area}, modulus={self.modulus}, force={self.force})"
