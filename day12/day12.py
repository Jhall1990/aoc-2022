import networkx as nx

def get_input(filename):
    with open(filename) as inp:
        return [i.strip() for i in inp.readlines()]


def reachable(cur_char, dest_char):
    if dest_char == "S":
        dest_char = "a"
    elif dest_char == "E":
        dest_char = "z"

    return ord(cur_char) >= ord(dest_char) - 1


def create_directed_graph(inp):
    # Sort of cheating using networkx but I don't feel like
    # implementing a directed graph myself
    graph = nx.DiGraph()
    start = None
    end = None
    edges = []
    alternate_starts = []

    def index(x, y):
        return str((y * len(inp[0])) + x)

    for y, line in enumerate(inp):
        for x, char in enumerate(line):
            idx = index(x, y)
            # See if it's the start coord
            if char == "S":
                start = idx
                char = "a"
            elif char == "E":
                end = idx
                char = "z"

            if char == "a":
                alternate_starts.append(idx)

            # Check up
            if y != 0 and reachable(char, inp[y - 1][x]):
                edges.append([idx, index(x, y - 1)])
            # Check down
            if y != len(inp) - 1 and reachable(char, inp[y + 1][x]):
                edges.append([idx, index(x, y + 1)])
            # Check left
            if x != 0 and reachable(char, inp[y][x - 1]):
                edges.append([idx, index(x - 1, y)])
            # Check right
            if x != len(inp[0]) - 1 and reachable(char, inp[y][x + 1]):
                edges.append([idx, index(x + 1, y)])

        graph.add_edges_from(edges)
    return graph, start, end, alternate_starts


if __name__ == "__main__":
    inp = get_input("input.txt")
    graph, start, end, alternate_starts = create_directed_graph(inp)
    print(len(nx.shortest_path(graph, start, end)) - 1)

    lowest = None
    for alt in alternate_starts:
        try:
            dist = len(nx.shortest_path(graph, alt, end)) - 1
        except nx.exception.NetworkXNoPath:
            # There is no path from that starting point
            continue

        if lowest is None:
            lowest = dist
        elif dist < lowest:
            lowest = dist
    print(lowest)

