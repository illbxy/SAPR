# utils/file_handler.py

import json

from models import Element, Node


def save_project(elements, nodes, filename):
    project_data = {
        'elements': [{'length': e.length, 'area': e.area, 'modulus': e.modulus, 'force': e.force} for e in elements],
        'nodes': [{'x': n.x, 'is_fixed': n.is_fixed, 'force': n.force} for n in nodes]
    }
    with open(filename, 'w') as file:
        json.dump(project_data, file, indent=4)

def load_project(filename):
    with open(filename, 'r') as file:
        project_data = json.load(file)
    elements = [Element(e['length'], e['area'], e['modulus'], e['force']) for e in project_data['elements']]
    nodes = [Node(n['x'], n['is_fixed'], n['force']) for n in project_data['nodes']]
    return elements, nodes
