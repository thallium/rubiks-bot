from typing import Dict, List
from ..geometry.group import Group
from ..geometry.grid import makeGrid

class RubiksCubeNet:
    def __init__(self, size: int, cubeWidth: float) -> None:
        U = makeGrid(cubeWidth, size)
        R = makeGrid(cubeWidth, size)
        F = makeGrid(cubeWidth, size)
        D = makeGrid(cubeWidth, size)
        L = makeGrid(cubeWidth, size)
        B = makeGrid(cubeWidth, size)

        self.U = Group(U)
        self.U.translate(0, -cubeWidth * 1.1)

        self.R = Group(R)
        self.R.translate(cubeWidth * 1.1, 0)

        self.F = Group(F)

        self.D = Group(D)
        self.D.translate(0, cubeWidth * 1.1)

        self.L = Group(L)
        self.L.translate(-cubeWidth * 1.1, 0)

        self.B = Group(B)
        self.B.translate(2 * 1.1 * cubeWidth, 0)

        self.stickers = [self.U, self.R, self.F, self.D, self.L, self.B]

        self.faces = {
            'U': self.U,
            'R': self.R,
            'F': self.F,
            'D': self.D,
            'L': self.L,
            'B': self.B,
        }

        self.group = Group(self.stickers)
        self.group.translate(cubeWidth * 1.1, cubeWidth * 1.1)

    @staticmethod
    def setFaceColors(faceStickers: Group, colors: List[str]):
        for i, g in enumerate(faceStickers.objects):
            g.color = colors[i]


    def setColors(self, colors: Dict[str, List[str]]):
        RubiksCubeNet.setFaceColors(self.U, colors['U'])
        RubiksCubeNet.setFaceColors(self.R, colors['R'])
        RubiksCubeNet.setFaceColors(self.F, colors['F'])
        RubiksCubeNet.setFaceColors(self.D, colors['D'])
        RubiksCubeNet.setFaceColors(self.L, colors['L'])
        RubiksCubeNet.setFaceColors(self.B, colors['B'])

    def getGroup(self) -> Group:
        self.stickers = [self.U, self.R, self.F, self.D, self.L, self.B]
        self.group = Group(self.stickers)
        return self.group
