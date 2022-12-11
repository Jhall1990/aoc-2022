def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]


UP    = "U"
DOWN  = "D"
LEFT  = "L"
RIGHT = "R"


class Node():
    def __init__(self, parent):
        self.parent = parent
        self.child = None
        self.x = 0
        self.y = 0

    def is_tail(self):
        return self.child is None


def create_worm(count):
    head = cur_node = Node(None)

    for _ in range(count - 1):
        node = Node(cur_node)
        cur_node.child = node
        cur_node = node
    return head


def is_touching(head_x, head_y, tail_x, tail_y):
    """
    Check if the tail is in any of the 8 spaces
    surrounding the head.
    """
    return ((head_x, head_y + 1) == (tail_x, tail_y) or     # Up
            (head_x, head_y - 1) == (tail_x, tail_y) or     # Down
            (head_x + 1, head_y) == (tail_x, tail_y) or     # Left
            (head_x - 1, head_y) == (tail_x, tail_y) or     # Right
            (head_x + 1, head_y - 1) == (tail_x, tail_y) or # Diagonal up/left
            (head_x - 1, head_y - 1) == (tail_x, tail_y) or # Diagonal up/right
            (head_x + 1, head_y + 1) == (tail_x, tail_y) or # Diagonal down/left
            (head_x - 1, head_y + 1) == (tail_x, tail_y))   # Diagonal down/right


def handle_diagonal(head_x, head_y, tail_x, tail_y):
    """
    Figure out which diagonal direction we should move the tail
    """
    if tail_y - 2 == head_y:
        direction = UP
    elif tail_y + 2 == head_y:
        direction = DOWN
    elif tail_x - 2 == head_x:
        direction = LEFT
    else:
        direction = RIGHT

    if direction == UP:
        return (tail_x + 1, tail_y - 1) if head_x > tail_x else (tail_x - 1, tail_y - 1)
    elif direction == DOWN:
        return (tail_x + 1, tail_y + 1) if head_x > tail_x else (tail_x - 1, tail_y + 1)
    elif direction == LEFT:
        return (tail_x - 1, tail_y + 1) if head_y > tail_y else (tail_x - 1, tail_y - 1)
    elif direction == RIGHT:
        return (tail_x + 1, tail_y + 1) if head_y > tail_y else (tail_x + 1, tail_y - 1)


def move_head(head_x, head_y, direction):
    if direction == UP:
        return head_x, head_y - 1
    elif direction == DOWN:
        return head_x, head_y + 1
    elif direction == LEFT:
        return head_x - 1, head_y
    else:
        return head_x + 1, head_y


def move_tail(head_x, head_y, tail_x, tail_y):
    # The head is on top of the tail
    if (head_x, head_y) == (tail_x, tail_y):
        return (tail_x, tail_y)

    # If the tail is in any of the 8 spaces surrounding head, do nothing
    if is_touching(head_x, head_y, tail_x, tail_y):
        return (tail_x, tail_y)

    # The head is on the same row, move towards it
    if head_y == tail_y:
        return (tail_x + 1, tail_y) if head_x > tail_x else (tail_x - 1, tail_y)

    # The head is in the same column, move towards it
    if head_x == tail_x:
        return (tail_x, tail_y + 1) if head_y > tail_y else (tail_x, tail_y - 1)

    # Handle diagonal
    return handle_diagonal(head_x, head_y, tail_x, tail_y)


def move_worm(visited, worm, direction):
    head = worm
    tail = worm.child

    head.x, head.y = move_head(head.x, head.y, direction)

    while tail is not None:
        new_x, new_y = move_tail(head.x, head.y, tail.x, tail.y)

        # If the tail didn't move, break no other segments will move
        if (new_x, new_y) == (tail.x, tail.y):
            break

        tail.x = new_x
        tail.y = new_y
        head = tail
        tail = tail.child


def do_moves(inp):
    head_x = head_y = 0
    tail_x = tail_y = 0
    visited = {(tail_x, tail_y)}

    for line in inp:
        direction, count = line.split()

        for _ in range(int(count)):
            head_x, head_y = move_head(head_x, head_y, direction)
            tail_x, tail_y = move_tail(head_x, head_y, tail_x, tail_y)
            visited.add((tail_x, tail_y))
    return len(visited)


def do_worm_moves(inp):
    worm = create_worm(10)
    tail = worm
    visited = set()

    while tail.child is not None:
        tail = tail.child

    for line in inp:
        direction, count = line.split()

        for _ in range(int(count)):
            move_worm(visited, worm, direction)
            visited.add((tail.x, tail.y))
    return len(visited)


if __name__ == "__main__":
    inp = get_input("input.txt")
    print(do_moves(inp))
    print(do_worm_moves(inp))
