import json
from models.node import Node
from models.rod import Rod
from models.load import Load


def save_data(file_name, nodes, rods, loads):
    """
    Сохраняет данные в файл.
    """
    data = {
        "nodes": [node.to_dict() for node in nodes],
        "rods": [rod.to_dict() for rod in rods],
        "loads": [load.to_dict() for load in loads],
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
        loads = [Load.from_dict(load_data) for load_data in data.get("loads", [])]

        return nodes, rods, loads
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise Exception(f"Ошибка загрузки данных: {e}")
