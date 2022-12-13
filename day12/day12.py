def get_input(filename):
    with open(filename) as inp:
        return [i.strip() for i in inp.readlines()]

def reachable(cur_char, dest_char):
    return ord(cur_char) >= ord(dest_char) - 1


def create_graph(inp):
    graph = {}
    start = None
    end = None

    for idy, line in enumerate(inp):
        for idx, char in enumerate(line):
            # See if it's the start coord
            if char == "S":
                start = (idx, idy)
                char = "a"
            elif char == "E":
                end = (idx, idy)
                char = "z"

            graph[(idx, idy)] = set()
            
            # Check up
            if idy != 0 and reachable(char, inp[idy - 1][idx]):
                graph[(idx, idy)].add((idx, idy - 1))
            # Check down
            if idy != len(inp) - 1 and reachable(char, inp[idy + 1][idx]):
                graph[(idx, idy)].add((idx, idy + 1))
            # Check left
            if idx != 0 and reachable(char, inp[idy][idx - 1]):
                graph[(idx, idy)].add((idx - 1, idy))
            # Check right
            if idx != len(inp[0]) - 1 and reachable(char, inp[idy][idx + 1]):
                graph[(idx, idy)].add((idx + 1, idy))
    return graph


if __name__ == "__main__":
    inp = get_input("input2.txt")
    graph = create_graph(inp)
