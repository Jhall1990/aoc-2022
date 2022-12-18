import os
import time


def get_input(filename):
    with open(filename) as inp:
        return [i.strip() for i in inp.readlines()]


class Wall():
    def __init__(self, segments):
        self.segments = segments

    def intersects(self, point):
        for i in range(len(self.segments) - 1):
            x_start = min(self.segments[i][0], self.segments[i + 1][0])
            x_end = max(self.segments[i][0], self.segments[i + 1][0])
            y_start = min(self.segments[i][1], self.segments[i + 1][1])
            y_end = max(self.segments[i][1], self.segments[i + 1][1])

            if (x_start <= point[0] <= x_end and
                y_start <= point[1] <= y_end):
                return True
        return False


class Board():
    FELL = -1
    SETTLED = -2
    OFF_GRID = -3

    def __init__(self):
        self.walls = []
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.sand = []

    def add_wall(self, segments):
        self.walls.append(Wall(segments))

        min_x = min(i[0] for i in segments)
        max_x = max(i[0] for i in segments)
        max_y = max(i[1] for i in segments)

        if min_x < self.min_x or not self.min_x:
            self.min_x = min_x
        if max_x > self.max_x or not self.max_x:
            self.max_x = max_x
        if max_y > self.max_y or not self.max_y:
            self.max_y = max_y

    def draw(self):
        os.system("clear")
        result = self.move_sand()

        for idy in range(self.min_y, self.max_y + 3):
            for idx in range(self.min_x - 6, self.max_x + 10):
                pt = (idx, idy)
                px = "."

                # See if the point is sand
                if pt in self.sand:
                    px = "o"

                # See if the point is a wall
                if self.intersects_wall(pt):
                    px = "#"
                print(px, end="")
            print()
        return result

    def add_sand(self, point):
        """
        Adds a grain of sand to the board and simulates it falling. If
        the sand settles within the board we return True, otherwise False.
        """
        self.sand.append(point)

    def intersects_wall(self, point):
        for wall in self.walls:
            if wall.intersects(point):
                return True

        # Also check the bottom wall
        if point[1] == self.max_y + 2:
            return True
        return False

    def intersects_sand(self, point):
        for grain in self.sand:
            if point == grain:
                return True
        return False

    def move_sand(self):
        """
        Simulate the sand falling 1 spot, return FELL if the sand is falling, return
        SETTLED if it hit a wall or another grain and can't move anymore, and return
        OFF_GRID if the sand is falling infinitely.
        """
        grain = self.sand[-1]
        pt_down = (grain[0], grain[1] + 1)
        pt_left = (grain[0] - 1, grain[1] + 1)
        pt_right = (grain[0] + 1, grain[1] + 1)

        if self.intersects_wall(pt_down) or self.intersects_sand(pt_down):
            if not self.intersects_wall(pt_left) and not self.intersects_sand(pt_left):
                self.sand[-1] = pt_left
                result = self.FELL
            elif not self.intersects_wall(pt_right) and not self.intersects_sand(pt_right):
                self.sand[-1] = pt_right
                result = self.FELL
            else:
                self.sand[-1] = grain
                result = self.SETTLED
        else:
            result = self.FELL
            self.sand[-1] = pt_down

        # If the sand settled at the (500, 0) we're done
        if self.sand[-1] == (500, 0):
            return self.OFF_GRID

        # See if we fell off the map
        if result == self.FELL and self.sand[-1][1] >= self.max_y + 2:
            return self.OFF_GRID
        return result


def parse_segments(line):
    segments = []
    for item in line.split(" -> "):
        segments.append(tuple(int(i) for i in item.split(",")))
    return segments


def create_board(inp):
    board = Board()
    for line in inp:
        segments = parse_segments(line)
        board.add_wall(segments)
    return board


def simulate_sand(board, point, draw=True):
    grains = 1
    board.add_sand(point)

    while True:
        if draw:
            grain_status = board.draw()
        else:
            grain_status = board.move_sand()

        if grain_status == Board.OFF_GRID:
            break
        elif grain_status == Board.SETTLED:
            grains += 1
            board.add_sand(point)
            if not draw:
                print(f"Adding grain {grains}")
    return grains


if __name__ == "__main__":
    inp = get_input("input.txt")
    board = create_board(inp)
    print(simulate_sand(board, (500, 0), draw=False))
