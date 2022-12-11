def get_input(pathname):
    with open(pathname, "r") as inp:
        return [i.strip() for i in inp]

def create_sets(line):
    left, right = line.split(",")
    a, b = left.split("-")
    left_set = set(range(int(a), int(b) + 1))
    a, b = right.split("-")
    right_set = set(range(int(a), int(b) + 1))
    return left_set, right_set


def overlapping_assignments(inp):
    total = 0

    for line in inp:
        left_set, right_set = create_sets(line)

        contains = False

        if len(left_set) == len(right_set):
            contains = right_set.issubset(left_set)
        elif len(left_set) > len(right_set):
            contains = right_set.issubset(left_set)
        else:
            contains = left_set.issubset(right_set)

        if contains:
            total += 1
    return total

def partially_overlapping_assignments(inp):
    total = 0

    for line in inp:
        left_set, right_set = create_sets(line)

        if left_set.intersection(right_set):
            total += 1
    return total


if __name__== "__main__":
    inp = get_input("input.txt")

    print(overlapping_assignments(inp))
    print(partially_overlapping_assignments(inp))
