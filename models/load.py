class Load:
    def __init__(self, load_type, force, direction):
        self.load_type = load_type
        self.force = force
        self.direction = direction

    def to_dict(self):
        return {
            "load_type": self.load_type,
            "force": self.force,
            "direction": self.direction,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["load_type"], data["force"], data["direction"])
