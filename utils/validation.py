def validate_data(project_data):
    for element in project_data["elements"]:
        if element["length"] <= 0 or element["area"] <= 0:
            return False, "Длина и площадь стержня должны быть положительными."
        if element["elasticity"] <= 0:
            return False, "Модуль упругости должен быть положительным."
        if element["stress_limit"] <= 0:
            return False, "Допускаемое напряжение должно быть положительным."

    for force in project_data["forces"]:
        if force["node"] < 0:
            return False, "Узел должен быть неотрицательным."
        if not isinstance(force["force"], (int, float)):
            return False, "Сила должна быть числом."

    return True, ""
