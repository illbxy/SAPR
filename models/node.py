class Node:
    def __init__(self, x):
        self.x = x

    def to_dict(self):
        """
        Преобразует объект в словарь.
        """
        return {"x": self.x}

    @classmethod
    def from_dict(cls, data):
        """
        Создает объект из словаря.
        """
        return cls(data["x"])
