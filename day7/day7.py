def get_input(filename):
    with open(filename, "r") as inp:
        return [i.strip() for i in inp.readlines()]

class File():
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)

    def __str__(self):
        return f"{self.name} {self.size}"


class Directory():
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = {}
        self.files = {}

    def add_file(self, name, size):
        file = File(name, size)
        self.files[name] = file

    def add_dir(self, directory):
        new_dir = Directory(self, directory)
        self.children[directory] = new_dir

    def size(self, size=0, cur_dir=None):
        if cur_dir is None:
            cur_dir = self

        if not cur_dir.children:
            size += sum(cur_dir.files[i].size for i in cur_dir.files)
            return size

        for dir_ in cur_dir.children:
            size += sum(cur_dir.files[i].size for i in cur_dir.files)
            size = cur_dir.size(size, cur_dir.children[dir_])
        return size

    def walk(self, depth=0, cur_dir=None):
        if cur_dir is None:
            cur_dir = self
            print(cur_dir.name)
            depth += 1
            cur_dir = self

        for dir_ in cur_dir.children:
            print(f"{' ' * (3 * depth)} {cur_dir.children[dir_].name}")
            for f in cur_dir.files:
                print(" " * (3 * (depth + 1)) + str(cur_dir.files[f]))
            self.walk(depth+1, cur_dir.children[dir_])


def create_directory_tree(inp):
    tree = Directory(None, "/")
    cur_dir = tree
    idx = 1

    while idx < len(inp):
        cmd = inp[idx].split()

        if cmd[0] == "$" and cmd[1] == "cd" and cmd[2] == "..":
            cur_dir = cur_dir.parent
            idx += 1
        elif cmd[0] == "$" and cmd[1] == "cd":
            cur_dir = cur_dir.children[cmd[2]]
            idx += 1
        elif cmd[0] == "$" and cmd[1] == "ls":
            idx += 1
            while idx < len(inp) and not inp[idx].startswith("$"):
                line_spl = inp[idx].split()
                if line_spl[0] == "dir":
                    cur_dir.add_dir(line_spl[1])
                else:
                    cur_dir.add_file(line_spl[1], line_spl[0])
                idx += 1
    return tree
        

if __name__ == "__main__":
    inp = get_input("input.txt")
    tree = create_directory_tree(inp)
    tree.walk()
    print(tree.size())
