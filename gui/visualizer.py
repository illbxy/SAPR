import matplotlib.pyplot as plt


def visualize_structure(nodes, elements, forces):
    """
    Визуализирует стержневую конструкцию и приложенные к ней нагрузки.

    :param nodes: Список узлов в формате [(x1, y1), (x2, y2), ...]
    :param elements: Список стержней в формате [(start_node, end_node), ...]
    :param forces: Список узловых нагрузок в формате [(node_index, force_value), ...]
    """
    if not nodes or not elements:
        raise ValueError("Данные для визуализации отсутствуют")

    fig, ax = plt.subplots(figsize=(8, 5))  # Устанавливаем размер графика

    # Визуализация стержней
    for start, end in elements:
        x_coords = [nodes[start][0], nodes[end][0]]
        y_coords = [nodes[start][1], nodes[end][1]]
        ax.plot(x_coords, y_coords, 'b-o',
                label="Стержень" if "Стержень" not in ax.get_legend_handles_labels()[1] else None)

    # Визуализация нагрузок
    for node_index, force_value in forces:
        x, y = nodes[node_index]
        direction = -0.5 if force_value < 0 else 0.5  # Стрелка вниз для отрицательных сил
        ax.arrow(x, y, 0, direction, head_width=0.2, head_length=0.2, fc='red', ec='red',
                 label="Сила" if "Сила" not in ax.get_legend_handles_labels()[1] else None)
        ax.text(x, y + direction * 1.2, f"{force_value:.2f} Н", color='red', ha='center', fontsize=9)

    # Настройки графика
    ax.set_title("Визуализация конструкции", fontsize=14)
    ax.set_xlabel("Координата X", fontsize=12)
    ax.set_ylabel("Координата Y", fontsize=12)
    ax.grid(True)
    ax.axis('equal')
    ax.legend()
    plt.show()
