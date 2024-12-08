# models/node.py

class Node:
    def __init__(self, x, is_fixed=False, force=None):
        self.x = x                # Координаты узла (по оси X)
        self.is_fixed = is_fixed  # Признак жесткой опоры
        self.force = force        # Сосредоточенная сила, приложенная к узлу (если есть)

    def __str__(self):
        return f"Node(x={self.x}, is_fixed={self.is_fixed}, force={self.force})"
