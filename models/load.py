class Load:
    def __init__(self, load_type, force, rod="-", node="-"):
        self.load_type = load_type
        self.force = force
        self.rod = rod
        self.node = node

    def to_dict(self):
        return {
            "load_type": self.load_type,
            "force": self.force,
            "rod": self.rod,
            "node": self.node,
        }

    @classmethod
    def from_dict(cls, data):
        return Load(
            data["load_type"],
            data["force"],
            data.get("rod", "-"),  # Добавлено
            data.get("node", "-"),  # Добавлено
        )
