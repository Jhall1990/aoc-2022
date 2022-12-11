def get_input(filename):
    with open(filename, "r") as inp:
        return inp.read().strip()

def find_first_packet(inp, width):
    idx = width
    while idx < len(inp):
        cur_chunk = inp[idx-width:idx]
        if len(set(cur_chunk)) == width:
            return idx
        idx += 1


if __name__ == "__main__":
    inp = get_input("input.txt")
    print(len(inp))
    print(find_first_packet(inp, 4))
    print(find_first_packet(inp, 14))
