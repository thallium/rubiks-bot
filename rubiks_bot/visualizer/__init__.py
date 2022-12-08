from PIL import Image, ImageDraw
from ..simulator.rubiksCubeSimulator import RubiksCubeSimulator
from ..puzzles.rubiksCubeNet import RubiksCubeNet

def render(fname, size: int, cubeWidth: float, alg: str):
    simulator = RubiksCubeSimulator(size)
    simulator.alg(alg)

    puzzleGeometry = RubiksCubeNet(size, cubeWidth)
    
    faceColors = simulator.getValues()
    puzzleGeometry.setColors(faceColors)

    colorTable = {
        'D': (255, 255, 0),
        'L': (255, 170, 0),
        'B': (0, 0, 255),
        'U': (255, 255, 255),
        'R': (255, 0, 0),
        'F': (0, 221, 0),
    }

    with Image.new("RGBA", (int(cubeWidth * 4.3), int(cubeWidth * 3.2))) as im:
        draw = ImageDraw.Draw(im)
        for group in puzzleGeometry.getGroup().objects:
            for obj in group.objects:
                draw.rectangle(
                    ((obj.x, obj.y), (obj.x + obj.length, obj.y + obj.length)),
                    fill=colorTable[obj.color],
                    outline=(0, 0, 0),
                    width=3)

        im.save(fname, format="PNG")
