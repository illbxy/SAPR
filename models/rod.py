class Rod:
    def __init__(self, length, area, modulus, stress):
        self.length = length
        self.area = area
        self.modulus = modulus
        self.stress = stress

    def to_dict(self):
        return {
            "length": self.length,
            "area": self.area,
            "modulus": self.modulus,
            "stress": self.stress,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["length"], data["area"], data["modulus"], data["stress"])
