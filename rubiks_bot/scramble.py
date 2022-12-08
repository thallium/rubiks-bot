from random import randint

scrambleLength = {
    2: (9, 9),
    3: (18, 22),
    4: (45, 47),
    5: (60, 60),
    6: (80, 80),
    7: (100, 100),
}

moves = [
    "F",
    "B",
    "R",
    "L",
    "U",
    "D",
]

def generateScramble(size: int):
    scramble = []
    minLength, maxLength = scrambleLength[size]
    length = randint(minLength, maxLength)

    last_move = -1
    for _ in range(length):
        while True:
            index = randint(0, 5)

            if index != last_move:
                move = moves[index]

                slices = randint(1, size // 2)
                if slices == 2:
                    move = move + "w"
                elif slices > 2:
                    move = f'{slices}{move}w'

                turn_type = randint(0, 2)
                if turn_type == 1: # reverse move
                    move += "'"
                elif turn_type == 2: # double move
                    move += "2"

                scramble.append(move)
                last_move = index
                break
    return ' '.join(scramble)
