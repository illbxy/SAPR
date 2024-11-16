import json

def save_project(file_path, nodes, elements, forces):
    data = {
        "nodes": nodes,
        "elements": [
            {
                "start_node": e[0],
                "end_node": e[1],
                "length": e[2],
                "area": e[3],
                "elasticity": e[4],
                "max_stress": e[5],
            } for e in elements
        ],
        "forces": forces
    }
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_project(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    nodes = data["nodes"]
    elements = [
        (
            e["start_node"],
            e["end_node"],
            e["length"],
            e["area"],
            e["elasticity"],
            e["max_stress"]
        ) for e in data["elements"]
    ]
    forces = data["forces"]
    return nodes, elements, forces
