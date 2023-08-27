class PointCord:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def as_arr(self):
        return [self.x, self.y]

    def to_str(self) -> str:
        return f"({self.x}, {self.y})"

