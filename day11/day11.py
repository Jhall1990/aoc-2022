def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]


class Monkey():
    def __init__(self):
        self.items = []
        self.oper = None
        self.test_val = None
        self.if_true = None
        self.if_false = None
        self.super_modulo = None
        self.inspect_count = 0

    def turn(self):
        item = self.items.pop(0)
        worry = self.inspect(item)
        to_monkey = self.if_true if self.test(worry) else self.if_false
        return worry, to_monkey

    def test(self, worry):
        return worry % self.test_val == 0

    def inspect(self, item):
        self.inspect_count += 1
        if self.super_modulo:
            return self.oper(item) % self.super_modulo
        return self.oper(item) // 3


def parse_operation(func):
    func_split = func.split()

    # Modifier is either an integer, or 'old' old just means
    # use the passed value again.
    try:
        modifier = int(func_split[4])
    except ValueError:
        modifier = None

    # Figure out what operation to take
    if func_split[3] == "+":
        return (lambda x: x + x) if modifier is None else (lambda x: x + modifier)
    elif func_split[3] == "*":
        return (lambda x: x * x) if modifier is None else (lambda x: x * modifier)


def create_monkeys(inp, super_mod=False):
    monkeys = []
    idx = 0
    cur_monkey = None

    while idx < len(inp):
        if inp[idx].startswith("Monkey"):
            cur_monkey = Monkey()
            monkeys.append(cur_monkey)
        elif inp[idx].startswith("Starting"):
            cur_monkey.items = [int(i) for i in inp[idx].split(":")[-1].split(",")]
        elif inp[idx].startswith("Operation"):
            cur_monkey.oper = parse_operation(inp[idx].split(":")[-1])
        elif inp[idx].startswith("Test"):
            cur_monkey.test_val = int(inp[idx].split()[-1])
        elif inp[idx].startswith("If true"):
            cur_monkey.if_true = int(inp[idx].split()[-1])
        elif inp[idx].startswith("If false"):
            cur_monkey.if_false = int(inp[idx].split()[-1])
        idx += 1

    # This is fucking dumb, really not sure how you are
    # supposed to figure this out
    if super_mod:
        super_modulo = 1
        for monkey in monkeys:
            super_modulo *= monkey.test_val

        for monkey in monkeys:
            monkey.super_modulo = super_modulo

    return monkeys


def do_rounds(monkeys, count):
    for n in range(count):
        for monkey in monkeys:
            # Skip any monkeys that have no items
            if not monkey.items:
                continue

            # Keep taking turns until the monkey has no more items
            while monkey.items:
                item, to_monkey = monkey.turn()
                monkeys[to_monkey].items.append(item)

    monkey_business = sorted([m.inspect_count for m in monkeys])
    return monkey_business[-1] * monkey_business[-2]


if __name__ == "__main__":
    inp = get_input("input.txt")
    monkeys = create_monkeys(inp)
    print(do_rounds(monkeys, 20))
    monkeys = create_monkeys(inp, super_mod=True)
    print(do_rounds(monkeys, 10000))
