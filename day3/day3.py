def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]


def char_val(char):
    # I don't feel like creating a map of char to
    # number so use ord and some math.
    if char.isupper():
        return ord(char) - 38
    else:
        return ord(char) - 96


def get_priorities(inp):
    total = 0
    for line in inp:
        left = set(line[0: int(len(line)/2)])
        right = set(line[int(len(line)/2)::])
        common = left.intersection(right)
        total += char_val(common.pop())
    return total


def get_priorities_by_group(inp, group_size=3):
    assert group_size > 1
    total = 0
    for idx in range(0, len(inp), group_size):
        inv = []
        for jdx in range(0, group_size):
            inv.append(set(inp[idx + jdx]))
        common = inv[0].intersection(*inv[1::]).pop()
        total += char_val(common)
    return total


if __name__ == "__main__":
    inp = get_input("input.txt")
    print(get_priorities(inp))
    print(get_priorities_by_group(inp))
