import functools
from typing import List, Dict, Tuple

TurnDefinition = List[Tuple[str, str]]

class Simulator:
    def __init__(self) -> None:
        self.stickers: Dict[str, str] = {}
        self.faces: Dict[str, List[str]] = {}
        self.turns: Dict[str, List[Tuple[str, str]]] = {}

    def addFace(self, stickers: List[str], label: str) -> Tuple[str, List[str]]:
        if label in self.faces:
            raise Exception(f'Face {label} already exists')
        if not label:
            label = str(len(self.faces) + 1)

        stickerIds = []
        for sticker in stickers:
            stickerId = str(len(self.stickers) + 1)
            self.stickers[stickerId] = sticker
            stickerIds.append(stickerId)

        self.faces[label] = stickerIds
        return label, stickerIds

    def addTurn(self, changes: List[Tuple[str, str]], label: str) -> str:
        if label in self.turns:
            raise Exception(f'Turn {label} already exists')
        if not label:
            label = str(len(self.turns) + 1)

        self.turns[label] = changes
        return label

    def doTurn(self, label: str, reverse: bool = False):
        changes = self.turns.get(label)

        if not changes:
            raise Exception(f'Unknown turn {label}')

        movingSticker = 1 if reverse else 0
        replacedSticker = 0 if reverse else 1

        cached: Dict[str, str] = {}
        for change in changes:
            cached[change[replacedSticker]] = self.stickers.get(change[replacedSticker])  # type: ignore
            self.stickers[change[replacedSticker]] = cached.get(change[movingSticker]) or self.stickers.get(change[movingSticker])  # type: ignore

    # def isSolved(self) -> bool:
        # for entry in self.faces.items():
            # stickerIds = entry.val

    def alg(self, alg: str):
        if not alg:
            return
        for turn in alg.split(' '):
            self.doTurn(turn)

    def getValues(self) -> Dict[str, List[str]]:
        return {
            key: [self.stickers[id] for id in stickerIds] for key, stickerIds in self.faces.items()
        }
