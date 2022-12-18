def get_input(filename):
    with open(filename) as inp:
        return [i.strip() for i in inp.realines()]

class Wall():
    def __init__(self, segments):
        self.segments = segments

    def intersects(self, point):
        pass


class Board():
    def __init__(self):
        self.walls = []
        self.left_edge = 0
        self.right_edge = 0
        self.top_edge = 0
        self.bottom_edge = 0

    def add_wall(segments):
        self.walls.append(Wall(segments))

        # TODO: Update the edges

    def draw(self):
        # TODO: Draw the board
        pass

    def add_sand(self, point):
        """
        Adds a grain of sand to the board and simulates it falling. If
        the sand settles within the board we return True, otherwise False.
        """
        pass
            


def parse_segments(line):
    segments = []
    for item in line.split(" -> "):
        segments.append((int(x), int(y) for x, y in item.split(",")))
    return segments


def create_board(inp):
    board = Board()
    for line in inp:
        segments = parse_segments(line)
        board.add_wall(segments)
    return board


def simulate_sand(board, point):
    grains = 0

    while True:
        if board.add_sand(point):
            grains += 0
        else:
            break
    return grains


if __name__ == "__main__":
    inp = get_input("input2.txt")
    board = create_board(inp)
    print(simulate_sand(board, (500, 0)))
