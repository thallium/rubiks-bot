from typing import List, Callable
from .simulator import Simulator, TurnDefinition
from .constants import CUBE_FACES, CUBE_AXIS, CUBE_AXIS_FACES, AXIS_ORIENTATION, AXIS_FACE_ORIENTATION, SIMULATOR_FACE
from ..algorithms.cube import parseCubeAlgorithm
from ..algorithms.algorithm import Turn, TurnType

class RubiksCubeSimulator(Simulator):
    def __init__(self, size: int) -> None:
        super().__init__()
        self.size: int = size
        self.gridSize: int = size * size

        for faceName in CUBE_FACES:
            self.addFace([faceName] * self.gridSize, faceName)
            self.addTurn(self.makeFaceTurnDefinitions(faceName), faceName)

        for axis in [CUBE_AXIS.X, CUBE_AXIS.Y, CUBE_AXIS.Z]:
            for column in range(self.size):
                layerChanges = []
                for i, faceName in enumerate(CUBE_AXIS_FACES[axis]):
                    nextFaceName = CUBE_AXIS_FACES[axis][(i + 1) % len(CUBE_AXIS_FACES[axis])]
                    nextFace = self.faces[nextFaceName]
                    currentFace = self.faces[faceName]

                    for row in range(self.size):
                        stickerIndex = row * self.size + column
                        sticker1 = currentFace[self.axisAlignedSticker(axis, faceName, stickerIndex)]
                        sticker2 = nextFace[self.axisAlignedSticker(axis, nextFaceName, stickerIndex)]
                        layerChanges.append((sticker1, sticker2))

                self.addTurn(layerChanges, f'{axis}-{column}')

    def makeFaceTurnDefinitions(self, faceName: str) -> TurnDefinition:
        stickerIds = self.faces[faceName]
        return [(stickerId, stickerIds[self.clockwiseSticker(i)]) for (i, stickerId) in enumerate(stickerIds)]

    def clockwiseSticker(self, stickerIndex: int) -> int:
        return (((stickerIndex + 1) * self.size) % (self.gridSize + 1)) - 1

    def counterClockwiseSticker(self, stickerIndex: int) -> int:
        return self.oppositeSticker(self.clockwiseSticker(stickerIndex))

    def oppositeSticker(self, stickerIndex: int) -> int:
        return self.gridSize - (stickerIndex + 1)

    def axisAlignedSticker(self, axis: str, face: str, stickerIndex: int):
        match AXIS_ORIENTATION[axis][face]:
            case 0:
                return stickerIndex
            case 1:
                return self.clockwiseSticker(stickerIndex)
            case 2:
                return self.oppositeSticker(stickerIndex)
            case -1:
                return self.counterClockwiseSticker(stickerIndex)
            case _:
                raise ValueError(f'Invalid axis face orientation value {AXIS_ORIENTATION[axis][face]}')

    def turnFace(self, face: str, axis: str, reverse: bool, From: int, to: int):
        if abs(to - From) >= self.size - 1:
            return

        self.doTurn(face, reverse)
        for layer in range(From, to + 1):
            self.doTurn(f'{axis}-{layer}', (not reverse) if AXIS_FACE_ORIENTATION[face] else reverse)

    def U(self, reverse: bool = False, layers: int = 1):
        self.turnFace(SIMULATOR_FACE.U, CUBE_AXIS.Y, reverse, self.size - layers, self.size - 1)

    def R(self, reverse: bool = False, layers: int = 1):
        self.turnFace(SIMULATOR_FACE.R, CUBE_AXIS.X, reverse, self.size - layers, self.size - 1)

    def B(self, reverse: bool = False, layers: int = 1):
        self.turnFace(SIMULATOR_FACE.B, CUBE_AXIS.Z, reverse, self.size - layers, self.size - 1)

    def F(self, reverse: bool = False, layers: int = 1):
        self.turnFace(SIMULATOR_FACE.F, CUBE_AXIS.Z, reverse, 0, layers - 1)

    def D(self, reverse: bool = False, layers: int = 1):
        self.turnFace(SIMULATOR_FACE.D, CUBE_AXIS.Y, reverse, 0, layers - 1)

    def L(self, reverse: bool = False, layers: int = 1):
        self.turnFace(SIMULATOR_FACE.L, CUBE_AXIS.X, reverse, 0, layers - 1)

    def M(self, reverse: bool = False):
        for layer in range(1, self.size - 1):
            self.doTurn(f'{CUBE_AXIS.X}-{layer}', not reverse)

    def S(self, reverse: bool = False):
        for layer in range(1, self.size - 1):
            self.doTurn(f'{CUBE_AXIS.Z}-{layer}', not reverse)

    def E(self, reverse: bool = False):
        for layer in range(1, self.size - 1):
            self.doTurn(f'{CUBE_AXIS.Y}-{layer}', not reverse)

    def X(self, reverse: bool = False):
        self.doTurn('R', reverse)
        self.doTurn('L', not reverse)
        for layer in range(0, self.size):
            self.doTurn(f'{CUBE_AXIS.X}-{layer}', reverse)

    def Y(self, reverse: bool = False):
        self.doTurn('U', reverse)
        self.doTurn('D', not reverse)
        for layer in range(0, self.size):
            self.doTurn(f'{CUBE_AXIS.Y}-{layer}', reverse)

    def Z(self, reverse: bool = False):
        self.doTurn('F', reverse)
        self.doTurn('B', not reverse)
        for layer in range(0, self.size):
            self.doTurn(f'{CUBE_AXIS.Z}-{layer}', reverse)

    def alg(self, alg: str):
        if not alg:
            return
        self.doTurns(parseCubeAlgorithm(alg))

    def doTurns(self, turns: List[Turn]):
        turnFunc = None
        for turn in turns:
            match turn.unit:
                case 'U':
                    turnFunc = self.U
                case 'R':
                    turnFunc = self.R
                case 'F':
                    turnFunc = self.F
                case 'D':
                    turnFunc = self.D
                case 'L':
                    turnFunc = self.L
                case 'B':
                    turnFunc = self.B
                case 'M':
                    turnFunc = self.M
                case 'E':
                    turnFunc = self.E
                case 'S':
                    turnFunc = self.S
                case 'x':
                    turnFunc = self.X
                case 'y':
                    turnFunc = self.Y
                case 'z':
                    turnFunc = self.Z

            reverse = turn.turnType == TurnType.CounterClockwise

            turnFunc(reverse, turn.slices)

            if turn.turnType == TurnType.Double:
                turnFunc(reverse, turn.slices)
