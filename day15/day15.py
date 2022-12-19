def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]


class Sensor():
    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.x = sensor_x
        self.y = sensor_y
        self.bcn_x = beacon_x
        self.bcn_y = beacon_y
        self.dist = self.get_dist((self.bcn_x, self.bcn_y))
        # Part 1
        # self.min_x = self.x - self.dist
        # self.max_x = self.x + self.dist
        # self.min_y = self.y - self.dist
        # self.max_y = self.y + self.dist

        # Part 2
        self.min = 0
        self.max = 4000000

        self.min_x = max((self.x - self.dist, self.min))
        self.max_x = min((self.x + self.dist, self.max))
        self.min_y = max((self.y - self.dist, self.min))
        self.max_y = min((self.y + self.dist, self.max))

    def get_dist(self, point):
        x_diff = abs(self.x - point[0])
        y_diff = abs(self.y - point[1])
        return x_diff + y_diff

    def points_on_row(self, row):
        if self.min_y <= row <= self.max_y:
            dist_to_y = self.get_dist((self.x, row))
            x_diff = self.dist - dist_to_y
            return max((self.x - x_diff, self.min)), min((self.x + x_diff, self.max))
        return None, None


def parse_coords(line):
    spl = line.split()
    sensor_x = int(spl[2].strip(",").split("=")[1])
    sensor_y = int(spl[3].strip(":").split("=")[1])
    beacon_x = int(spl[8].strip(",").split("=")[1])
    beacon_y = int(spl[9].split("=")[1])
    return sensor_x, sensor_y, beacon_x, beacon_y


def create_sensors(inp):
    sensors = []
    for line in inp:
        sensors.append(Sensor(*parse_coords(line)))
    return sensors


def combine_ranges(points):
    """
    Create a list of range lists [(a, b), (c, d)] that is
    a combination of all the provided points.
    """
    combined = []

    for start, end in sorted(points):
        if combined and combined[-1][1] >= start - 1:
            combined[-1][1] = max(combined[-1][1], end)
        else:
            combined.append([start, end])
    return combined


def num_points_with_no_beacon(sensors, row):
    points = set()

    for sensor in sensors:
        start, end = sensor.points_on_row(row)
        if start is not None and end is not None:
            points.add((start, end))

    return sum(len(range(i[0], i[1])) for i in combine_ranges(points)), points


def point_with_beacon(sensors):
    min_count = 4000000
    for i in range(3000000, 4000000):
        print(i)
        num_points, points = num_points_with_no_beacon(sensors, i)
        if num_points < min_count:
            print(combine_ranges(points))
            break


if __name__ == "__main__":
    inp = get_input("input.txt")
    sensors = create_sensors(inp)
    # print(num_points_with_no_beacon(sensors, 2000000))
    point_with_beacon(sensors)
