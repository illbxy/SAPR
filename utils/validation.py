def validate_data(nodes_data, elements_data):
    if not nodes_data or not elements_data:
        print("Ошибка: Пустые данные для узлов или стержней.")
        return False
    return True
