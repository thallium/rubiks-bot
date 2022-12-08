from typing import List
from .sticker import Sticker

def makeGrid(length: float, size: int):
    elementWidth = length / size
    stickers = []
    for i in range(0, size):
        stickers.extend(makeRow(length, size, elementWidth * i))
    return stickers

def makeRow(length: float, size: int, vOffset: float) -> List[Sticker]:
    elementWidth = length / size
    return [Sticker(elementWidth * i, vOffset, elementWidth) for i in range(size)]
