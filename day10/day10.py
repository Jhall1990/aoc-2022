def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]


INS_NOOP = "noop"
INS_ADDX = "addx"


class Instruction():
    def __init__(self, cycles, func):
        self.cycles = cycles
        self.func = func
        self.done = False
        self.name = None

    def cycle(self):
        self.cycles -= 1

        if self.cycles == 0:
            self.func()
            self.done = True

class Noop(Instruction):
    def __init__(self):
        super().__init__(1, lambda: None)
        self.name = "noop"


class Addx(Instruction):
    def __init__(self, func):
        super().__init__(2, func)
        self.name = "addx"


class CPU():
    def __init__(self, crt):
        self.pc = 0
        self.x = 1
        self.ins = []
        self.current_ins = None
        self.signal_strength = 0
        self.crt = crt

    def add_instruction(self, ins, arg=None):
        if ins == INS_NOOP:
            self.ins.append(Noop())
        elif ins == INS_ADDX:
            self.ins.append(Addx(lambda: self.increment_reg("x", int(arg))))

    def increment_reg(self, reg, val):
        register = getattr(self, reg)
        setattr(self, reg, register + val)

    def cycle(self):
        self.pc += 1
        self.set_signal_strength()
        self.crt.update(self.x)

        # If we aren't executing an instruction, start
        # the next one
        if self.current_ins is None:
            self.current_ins = self.ins.pop(0)

        self.current_ins.cycle()

        if self.current_ins.done:
            self.current_ins = None

        return bool(self.ins) or bool(self.current_ins)

    def set_signal_strength(self):
     self.signal_strength = self.pc * self.x


class CRT():
    def __init__(self):
        self.pc = 0
        self.px = ["." for _ in range(240)]

    def update(self, reg):
        px_on_line = self.pc % 40
        if (px_on_line == reg - 1 or
            px_on_line == reg or
            px_on_line == reg + 1):
            self.px[self.pc] = "#"

        self.pc += 1

    def draw(self):
        for i in range(6):
            print("".join(self.px[0 + (40 * i): 40 + (40 * i)]))


def add_and_execute(inp, sum_cycles):
    crt = CRT()
    cpu = CPU(crt)
    signal_sum = 0


    for line in inp:
        line_split = line.split()
        
        if len(line_split) == 1:
            cpu.add_instruction(line_split[0])
        elif len(line_split) == 2:
            cpu.add_instruction(line_split[0], line_split[1])

    in_progress = True
    while in_progress:
        in_progress = cpu.cycle()

        if cpu.pc in sum_cycles:
            signal_sum += cpu.signal_strength

    crt.draw()
    return signal_sum


if __name__ == "__main__":
    inp = get_input("input.txt")
    sum_cycles = [20, 60, 100, 140, 180, 220]
    print(add_and_execute(inp, sum_cycles))
