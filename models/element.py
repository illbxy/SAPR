class Element:
    def __init__(self, node_start, node_end, length, area, elasticity, stress_limit):
        self.node_start = node_start
        self.node_end = node_end
        self.length = length
        self.area = area
        self.elasticity = elasticity
        self.stress_limit = stress_limit

    def __repr__(self):
        return (f"Element(start={self.node_start}, end={self.node_end}, "
                f"length={self.length}, area={self.area}, "
                f"elasticity={self.elasticity}, stress_limit={self.stress_limit})")
