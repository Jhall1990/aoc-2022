def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]


def visible_trees(inp):
    visible = set()
    check_up_down(visible, inp)
    check_up_down(visible, inp, reverse=True)
    check_left_right(visible, inp)
    check_left_right(visible, inp, reverse=True)

    # Include all the trees at the top and bottom of the grid
    visible_top_bottom = len(inp[0]) * 2

    # Include all the trees along the left and right, minus the ones
    # we already counted above.
    visible_left_right = (len(inp) - 2) * 2
    return len(visible) + visible_top_bottom + visible_left_right


def check_up_down(visible, inp, reverse=False):
    """
    Find trees visible in each column. If reverse is False start
    from the top, otherwise start from the bottom.
    """
    x = 1
    y = 1 if not reverse else len(inp) - 2
    update = lambda n: (n + 1) if not reverse else (n - 1)
    y_break = lambda n: (n < len(inp) - 1) if not reverse else (n > 0)

    while x < len(inp[0]) - 1:
        tallest_tree = int(inp[y-1][x]) if not reverse else int(inp[y+1][x])

        while y_break(y):
            cur_tree = int(inp[y][x])

            if cur_tree > tallest_tree:
                visible.add((x, y))
                tallest_tree = cur_tree

            # No need to keep looking if we see a 9, no tree can be taller
            if tallest_tree == 9:
                break
            y = update(y)
        x += 1
        y = 1 if not reverse else len(inp) - 2


def check_left_right(visible, inp, reverse=False):
    """
    Find trees visible in each row. If reverse is Flase start from
    the left, otherwise start from the right.
    """
    x = 1 if not reverse else len(inp[0]) - 2
    y = 1
    update = lambda n: (n + 1) if not reverse else (n - 1)
    x_break = lambda n: (n < len(inp[0]) - 1) if not reverse else (n > 0)

    while y < len(inp) - 1:
        tallest_tree = int(inp[y][x-1]) if not reverse else int(inp[y][x+1])

        while x_break(x):
            cur_tree = int(inp[y][x])

            if cur_tree > tallest_tree:
                visible.add((x, y))
                tallest_tree = cur_tree

            # No need to keep looking if we see a 9, no tree can be taller
            if tallest_tree == 9:
                break
            x = update(x)
        y += 1
        x = 1 if not reverse else len(inp[0]) - 2


def scenic_score(inp, x, y):
    mod_x = x
    mod_y = y

    # Check up
    up = 0
    mod_y -= 1
    while mod_y >= 0:
        up += 1
        if int(inp[mod_y][x]) >= int(inp[y][x]):
            break
        mod_y -= 1

    # Check down
    down = 0
    mod_y = y + 1
    while mod_y < len(inp):
        down += 1
        if int(inp[mod_y][x]) >= int(inp[y][x]):
            break
        mod_y += 1

    # Check left
    left = 0
    mod_x -= 1
    while mod_x >= 0:
        left += 1
        if int(inp[y][mod_x]) >= int(inp[y][x]):
            break
        mod_x -= 1

    # Check right
    right = 0
    mod_x = x + 1
    while mod_x < len(inp[0]):
        right += 1
        if int(inp[y][mod_x]) >= int(inp[y][x]):
            break
        mod_x += 1
    
    return up * down * left * right


def highest_scenic_score(inp):
    high = 0
    x = y = 1

    while y < len(inp) - 1:
        while x < len(inp[0]) - 1:
            score = scenic_score(inp, x, y)
            if score > high:
                high = score
            x += 1
        y += 1
        x = 1
    return high



if __name__ == "__main__":
    inp = get_input("input.txt")
    print(visible_trees(inp))
    print(highest_scenic_score(inp))

