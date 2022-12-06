def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip("\n") for i in inp]


def get_stacks(inp):
    # We need to know how many lists to create intially which
    # is len(line) / 4 + 1, as there are 4 characters in total for
    # each column - 1 for the last as there is no space after it
    # which is why we add 1.
    stacks = []
    for i in range(len(inp[0]) // 4 + 1):
        stacks.append([])

    for line_num, line in enumerate(inp):
        idx = 0
        while idx * 4 + 1 < len(line):
            char = line[idx * 4 + 1]
            if char.isnumeric():
                # We hit the end of the boxes, return the line
                # number + 2 so we know where to start parsing moves.
                return stacks, line_num + 2
            if char != " ":
                stacks[idx].append(char)
            idx += 1
    raise Exception("We shouldn't get here")


def move_box(stacks, to, frm):
    move = stacks[frm].pop(0)
    stacks[to].insert(0, move)


def do_moves(inp, stacks, start):
    for move in inp[start::]:
        instructions = move.split()
        num_moves = int(instructions[1])
        frm = int(instructions[3]) - 1
        to = int(instructions[5]) - 1

        for _ in range(num_moves):
            move_box(stacks, to, frm)

    return "".join(i[0] for i in stacks)

def move_together(stacks, count, to, frm):
    to_move = []
    for _ in range(count):
        mv = stacks[frm].pop(0)
        to_move.append(mv)

    for item in reversed(to_move):
        stacks[to].insert(0, item)


def do_moves_together(inp, stacks, start):
    for move in inp[start::]:
        instructions = move.split()
        num_moves = int(instructions[1])
        frm = int(instructions[3]) - 1
        to = int(instructions[5]) - 1
        move_together(stacks, num_moves, to, frm)

    return "".join(i[0] for i in stacks)


if __name__ == "__main__":
    inp = get_input("input.txt")
    stacks, move_line = get_stacks(inp)
    print(do_moves(inp, stacks, move_line))

    # I don't feel like copying so just parse the input again
    stacks, move_line = get_stacks(inp)
    print(do_moves_together(inp, stacks, move_line))
