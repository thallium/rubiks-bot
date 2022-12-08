from enum import Enum
from typing import List

class SIMULATOR_FACE:
    U = "U"
    R = "R"
    F = "F"
    D = "D"
    L = "L"
    B = "B"

CUBE_FACES: List[str] = [
    SIMULATOR_FACE.U,
    SIMULATOR_FACE.R,
    SIMULATOR_FACE.F,
    SIMULATOR_FACE.D,
    SIMULATOR_FACE.L,
    SIMULATOR_FACE.B,
]

class CUBE_AXIS:
    X = "X"
    Y = "Y"
    Z = "Z"

# Faces that wrap around a given axis
CUBE_AXIS_FACES = {
    'X': [SIMULATOR_FACE.U, SIMULATOR_FACE.B, SIMULATOR_FACE.D, SIMULATOR_FACE.F],
    'Y': [SIMULATOR_FACE.L, SIMULATOR_FACE.B, SIMULATOR_FACE.R, SIMULATOR_FACE.F],
    'Z': [SIMULATOR_FACE.L, SIMULATOR_FACE.U, SIMULATOR_FACE.R, SIMULATOR_FACE.D],
}

AXIS_ORIENTATION = {
    'X': {
        SIMULATOR_FACE.U: 0,
        SIMULATOR_FACE.B: 2,
        SIMULATOR_FACE.F: 0,
        SIMULATOR_FACE.D: 0,
    },
    'Y': {
        SIMULATOR_FACE.B: -1,
        SIMULATOR_FACE.F: -1,
        SIMULATOR_FACE.L: -1,
        SIMULATOR_FACE.R: -1,
    },
    'Z': {
        SIMULATOR_FACE.U: -1,
        SIMULATOR_FACE.D: 1,
        SIMULATOR_FACE.L: 2,
        SIMULATOR_FACE.R: 0,
    },
}

# True if faces are in reverse orientation
# from the axis it's on (X, Y, Z).
# For example D turns on the Y axis, but the
# y axis layer turns clockwise based on the U
# face, so D needs to be reversed
AXIS_FACE_ORIENTATION = {
  SIMULATOR_FACE.U: False,
  SIMULATOR_FACE.R: False,
  SIMULATOR_FACE.F: False,
  SIMULATOR_FACE.D: True,
  SIMULATOR_FACE.L: True,
  SIMULATOR_FACE.B: True,
}
