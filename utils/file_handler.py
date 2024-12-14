import json
from models.node import Node
from models.rod import Rod
from models.load import Load


def save_data(file_name, nodes, rods, loads, supports, modulus_of_elasticity):
    """
    Сохраняет данные в файл.
    """
    data = {
        "nodes": [node.to_dict() for node in nodes],
        "rods": [rod.to_dict() for rod in rods],
        "loads": [load.to_dict() for load in loads],
        "supports": supports,  # Добавлено для опор
        "modulus_of_elasticity": modulus_of_elasticity  # Добавлено для модуля упругости
    }
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def load_data(file_name):
    """
    Загружает данные из файла.
    """
    try:
        with open(file_name, "r") as file:
            data = json.load(file)

        nodes = [Node.from_dict(node_data) for node_data in data.get("nodes", [])]
        rods = [Rod.from_dict(rod_data) for rod_data in data.get("rods", [])]
        loads = [Load.from_dict(load_data) for load_data in data.get("loads", [])]  # Обновлено
        supports = data.get("supports", {"left": False, "right": False})  # Опоры
        modulus_of_elasticity = data.get("modulus_of_elasticity", 0)  # Модуль упругости

        return nodes, rods, loads, supports, modulus_of_elasticity
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise Exception(f"Ошибка загрузки данных: {e}")
