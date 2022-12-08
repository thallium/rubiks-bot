import re
from typing import List
from .algorithm import Turn, TurnType

class TurnAbbreviation:
    Clockwise = ""
    CounterClockwise = "'"
    Double = "2"

cubeTurnRegex = re.compile('([0-9]+)?([UuFfRrDdLlBbMESxyz])(w)?([2\'])?')

def parseCubeAlgorithm(algorithm: str) -> List[Turn]:
    if not algorithm:
        return []

    turns: List[Turn] = []
    for match in cubeTurnRegex.finditer(algorithm):
        rawSlices = match.group(1)
        rawFace = match.group(2)
        outerBlockIndicator = match.group(3)
        rawType = match.group(4) or TurnAbbreviation.Clockwise
        isLowerCaseMove = 'ufrdlb'.find(rawFace) != -1
        if isLowerCaseMove:
            rawFace = rawFace.upper()
        turns.append(Turn(rawFace, getTurnType(rawType), 2 if isLowerCaseMove else getSlices(rawSlices, outerBlockIndicator)))

    return turns

def getSlices(rawSlices: str, outerBlockIndicator: str) -> int:
    if outerBlockIndicator and not rawSlices:
        return 2
    if not outerBlockIndicator and rawSlices:
        raise ValueError("Invalid move: Cannot specify num slices if outer block move indicator 'w' is not present")
    if not outerBlockIndicator and not rawSlices:
        return 1
    intValue = int(rawSlices)
    if intValue > 1:
        return intValue

    raise ValueError(f"Invalid outer block move ({intValue}) must be greater than 1")

def getTurnType(rawType: str) -> TurnType:
    match rawType:
        case TurnAbbreviation.Clockwise:
            return TurnType.Clockwise
        case TurnAbbreviation.CounterClockwise:
            return TurnType.CounterClockwise
        case TurnAbbreviation.Double:
            return TurnType.Double
