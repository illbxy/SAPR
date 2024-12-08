from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtCore import QRectF

class Visualizer:
    def __init__(self, parent):
        self.parent = parent

    def visualize(self, nodes_data, elements_data, scene):
        try:
            # Очищаем сцену перед новой визуализацией
            scene.clear()

            # Рисуем узлы
            for node in nodes_data:
                coords = node[0].split(',')
                x, y = float(coords[0]), float(coords[1])
                ellipse = QGraphicsEllipseItem(QRectF(x * 50, y * 50, 10, 10))  # Увеличиваем масштаб для видимости
                scene.addItem(ellipse)

            # Рисуем стержни
            for element in elements_data:
                length = float(element[0])
                x1, y1 = 0, 0  # Начальные координаты
                x2, y2 = length, 0  # Конечные координаты
                line = QGraphicsLineItem(x1 * 50, y1 * 50, x2 * 50, y2 * 50)  # Масштабирование
                scene.addItem(line)

            print("Визуализация завершена.")

        except Exception as e:
            print(f"Ошибка при визуализации: {e}")
