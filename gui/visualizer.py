import math

from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, \
    QGraphicsPolygonItem
from PyQt5.QtGui import QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, QPointF

def plot_structure(scene, nodes, rods, loads, left_support = False, right_support = False):

    # Проверка значений флагов
    print(f"Левая опора: {left_support}, Правая опора: {right_support}")

    if scene is None:
        print("Ошибка: графическая сцена не инициализирована.")
        return

    scene.clear()  # Очищаем сцену перед построением

    # Настройка визуализации
    node_radius = 5
    pen_node = QPen(Qt.blue, 2)  # Узлы
    pen_rod = QPen(Qt.black, 2)  # Стержни
    pen_concentrated = QPen(Qt.red, 3)  # Цвет для сосредоточенных нагрузок
    pen_distributed = QPen(Qt.blue, 3)  # Цвет для распределённых нагрузок
    pen_support = QPen(Qt.darkGray, 2)  # Цвет для опор

    # Визуализация узлов
    node_positions = {}
    for i, node in enumerate(nodes):
        x = node.x
        node_positions[i] = (x * 50 , 0)
        print(f"Добавление узла {i+1}: x = {x}, y = 0")

        #Создание графического элемента - окружности
        ellipse = QGraphicsEllipseItem(
            x * 50 - node_radius + 2.5,
            -node_radius,
            node_radius,
            node_radius
        )

        ellipse.setBrush(QColor(Qt.blue))
        ellipse.setPen(pen_node)
        ellipse.setZValue(3)  # Узлы выше стержней
        scene.addItem(ellipse)

    # Визуализация стержней с ограничением длины и площади
    for i, rod in enumerate(rods):
        if i not in node_positions or (i + 1) not in node_positions:
            print(f"Ошибка: узлы для стержня {i + 1} не найдены.")
            continue

        try:
            # Начальный и конечный узлы стержня
            x1, y1 = node_positions[i]
            x2, y2 = node_positions[i + 1]

            # Длина стержня
            rod_length = abs(x2-x1)

            # Ограничение площади стержня
            rod_height = min(math.sqrt(rod.area) * 30, 150)

            # Построение прямоугольного стержня
            rect = QGraphicsRectItem(x1, -rod_height/2 - 2.5, rod_length, rod_height)
            rect.setPen(pen_rod)
            rect.setBrush(Qt.transparent)
            rect.setZValue(2)  # Стержни ниже узлов
            scene.addItem(rect)

            print(f"Стержень {i+1} успешно добавлен")

        except Exception as e:
            print(f"Ошибка обработки стержней: {e}")


    # Визуализация нагрузок
    for load in loads:
        print(f"Обработка нагрузки: {vars(load)}")  # Проверка, что нагрузка передается в функцию

        try:
            # Проверка, что нагрузка имеет необходимый тип
            if not hasattr(load, 'load_type') or not (hasattr(load, 'node') or hasattr(load, 'rod')) or not hasattr(load, 'force'):
                print(f"Ошибка: неверные атрибуты у нагрузки {load}")
                continue

            # Определение координат узла, к которому относится нагрузка
            if load.load_type == 'Сосредоточенная':
                node_idx = int(load.node) - 1
                if node_idx in node_positions:
                    x, y = node_positions[node_idx]

                    # Направление и величина силы
                    direction = 1 if load.force >= 0 else -1
                    arrow_length = 30  # Длина стрелки нагрузки

                    # Рисуем сосредоточенную нагрузку
                    arrow = QGraphicsLineItem(x, y - 2.5, x + arrow_length * direction, y - 2.5)
                    arrow.setPen(pen_concentrated)
                    arrow.setZValue(1)
                    scene.addItem(arrow)

                    # Рисуем стрелку в конце линии
                    arrowhead_size = 5  # Размер стрелки
                    if direction > 0:  # Стрелка вправо
                        arrowhead = QPolygonF([
                            QPointF(x + arrow_length * direction, y - 2.5),  # Конец линии
                            QPointF(x + arrow_length * direction - arrowhead_size, y - 2.5 - arrowhead_size / 2),
                            QPointF(x + arrow_length * direction - arrowhead_size, y - 2.5 + arrowhead_size / 2)
                        ])
                    else:  # Стрелка влево
                        arrowhead = QPolygonF([
                            QPointF(x + arrow_length * direction, y - 2.5),  # Конец линии
                            QPointF(x + arrow_length * direction + arrowhead_size, y - 2.5 - arrowhead_size / 2),
                            QPointF(x + arrow_length * direction + arrowhead_size, y - 2.5 + arrowhead_size / 2)
                        ])

                    arrow_head_item = QGraphicsPolygonItem(arrowhead)
                    arrow_head_item.setBrush(QColor(Qt.red))  # Цвет стрелки
                    arrow_head_item.setPen(pen_concentrated)
                    scene.addItem(arrow_head_item)

                print(f"Сосредоточенная нагрузка на узле {node_idx + 1}: сила = {load.force}")

            elif load.load_type == 'Продольная':
                rod_idx = int(load.rod) - 1
                if rod_idx in node_positions and rod_idx + 1 in node_positions:
                    # Извлекаем координаты начала и конца стержня
                    x_start, y_start = node_positions[rod_idx]
                    x_end, y_end = node_positions[rod_idx + 1]

                    # Распределяем нагрузку вдоль стержня
                    step = 20  # Шаг стрелок вдоль стержня
                    for x in range(int(x_start), int(x_end), step):
                        arrow = QGraphicsLineItem(x, y_start - 2.5, x + 10, y_start - 2.5)
                        arrow.setPen(pen_distributed)
                        arrow.setZValue(1)
                        scene.addItem(arrow)

                        # Направление стрелки
                        arrowhead_size = 5
                        if load.force >= 0:  # Стрелка вправо
                            arrowhead = QPolygonF([
                                QPointF(x + 10, y_start - 2.5),  # Конец линии
                                QPointF(x + 10 - arrowhead_size, y_start - 2.5 - arrowhead_size / 2),
                                QPointF(x + 10 - arrowhead_size, y_start - 2.5 + arrowhead_size / 2)
                            ])
                        else:  # Стрелка влево
                            arrowhead = QPolygonF([
                                QPointF(x + 10, y_start - 2.5),  # Конец линии
                                QPointF(x + 10 + arrowhead_size, y_start - 2.5 - arrowhead_size / 2),
                                QPointF(x + 10 + arrowhead_size, y_start - 2.5 + arrowhead_size / 2)
                            ])

                        arrow_head_item = QGraphicsPolygonItem(arrowhead)
                        arrow_head_item.setBrush(QColor(Qt.blue))  # Цвет стрелки
                        arrow_head_item.setPen(pen_distributed)
                        scene.addItem(arrow_head_item)

                    print(f"Распределённая нагрузка на стержне {rod_idx + 1}: сила = {load.force}")

        except Exception as e:
            print(f"Ошибка обработки нагрузки: {e}")

    # Визуализация опор
    support_angle = 45  # Угол наклона линии опоры (градусы)
    support_step = 15  # Расстояние между черточками
    support_length = 20  # Длина одной черточки

    def draw_support(x, y, direction):
        """Рисует опору в виде нескольких черточек."""
        num_lines = 5  # Количество черточек в опоре
        for i in range(num_lines):
            y_offset = i * support_step
            x_start = x
            y_start = y  + y_offset - 35
            x_end = x + direction * support_length * math.cos(math.radians(support_angle))
            y_end = y_start + support_length * math.sin(math.radians(support_angle))

            line = QGraphicsLineItem(x_start, y_start, x_end, y_end)
            line.setPen(pen_support)
            line.setZValue(1)  # Опоры ниже нагрузок
            scene.addItem(line)

    if left_support:
        print("Добавление левой опоры")
        x, y = node_positions[0]  # Координаты первого узла
        draw_support( x, y, direction=-1)  # Черточки наклонены влево

    if right_support:
        print("Добавление правой опоры")
        x, y = node_positions[len(node_positions) - 1]  # Координаты последнего узла
        draw_support(x, y, direction=1)  # Черточки наклонены вправо

