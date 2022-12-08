class Group:
    def __init__(self, objects) -> None:
        self.objects = objects

    def translate(self, x: float, y: float):
        for o in self.objects:
            o.translate(x, y)
