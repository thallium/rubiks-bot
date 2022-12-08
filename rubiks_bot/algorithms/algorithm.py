from enum import Enum

class TurnType(Enum):
    Clockwise = 0
    CounterClockwise = 1
    Double = 2


class Turn:
    def __init__(self, unit: str, turnType: TurnType, slices: int, n: int = 1) -> None:
        self.unit = unit
        self.turnType = turnType
        self.slices = slices
        self.n = n
