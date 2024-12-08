# visualizer.py

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

class Visualizer:
    def __init__(self, graphics_view):
        """
        Инициализирует визуализатор с заданным QGraphicsView.
        """
        self.graphics_view = graphics_view
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

    def visualize(self, data):
        """
        Метод визуализации данных.
        """
        self.scene.clear()  # Очистить предыдущую сцену
        # Реализация визуализации
        for element in data:
            # Пример: добавление элементов на сцену
            self.scene.addText(str(element))
        self.graphics_view.show()
