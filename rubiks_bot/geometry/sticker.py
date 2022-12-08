class Sticker:
    def __init__(self, x: float, y: float, length: float) -> None:
        self.x = x
        self.y = y
        self.length = length

    def translate(self, x: float, y: float):
        self.x += x
        self.y += y
