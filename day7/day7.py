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

    def size(self, cur_dir, size=0):
        size += sum(cur_dir.files[i].size for i in cur_dir.files)

        if not cur_dir.children:
            return size

        for dir_ in cur_dir.children:
            size = cur_dir.size(cur_dir.children[dir_], size)
        return size

    def bf_search(self, max_size):
        total = 0
        def search(total, dirs, max_size):
            new_dirs = []
            for dir_ in dirs:
                new_dirs += [dir_.children[i] for i in dir_.children]

                size = dir_.size(dir_)
                if size <= max_size:
                    total += size

            if not new_dirs:
                return total
            total = search(total, new_dirs, max_size)
            return total
        search(total, [self.children[i] for i in self.children], max_size)
        return total


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


def test_tree():
    tree = Directory(None, "/")
    tree.add_file("a", 1000)
    tree.add_file("b", 1000)
    tree.add_file("c", 1000)
    tree.add_dir("a")
    tree.children["a"].add_dir("a")
    tree.children["a"].children["a"].add_file("a", 1000)
    tree.children["a"].children["a"].add_file("b", 1000)
    tree.children["a"].children["a"].add_file("c", 1000)
    tree.children["a"].add_dir("b")
    tree.children["a"].children["b"].add_file("a", 1000)
    tree.children["a"].children["b"].add_file("b", 1000)
    tree.children["a"].children["b"].add_file("c", 1000)
    tree.children["a"].add_dir("c")
    tree.children["a"].children["c"].add_file("a", 1000)
    tree.children["a"].children["c"].add_file("b", 1000)
    tree.children["a"].children["c"].add_file("c", 1000)

    tree.add_dir("b")
    tree.children["b"].add_dir("a")
    tree.children["b"].children["a"].add_file("a", 1000)
    tree.children["b"].children["a"].add_file("b", 1000)
    tree.children["b"].children["a"].add_file("c", 1000)
    tree.children["b"].add_dir("b")
    tree.children["b"].children["b"].add_file("a", 1000)
    tree.children["b"].children["b"].add_file("b", 1000)
    tree.children["b"].children["b"].add_file("c", 1000)
    tree.children["b"].add_dir("c")
    tree.children["b"].children["c"].add_file("a", 1000)
    tree.children["b"].children["c"].add_file("b", 1000)
    tree.children["b"].children["c"].add_file("c", 1000)

    tree.add_dir("c")
    tree.children["c"].add_dir("a")
    tree.children["c"].children["a"].add_file("a", 1000)
    tree.children["c"].children["a"].add_file("b", 1000)
    tree.children["c"].children["a"].add_file("c", 1000)
    tree.children["c"].add_dir("b")
    tree.children["c"].children["b"].add_file("a", 1000)
    tree.children["c"].children["b"].add_file("b", 1000)
    tree.children["c"].children["b"].add_file("c", 1000)
    tree.children["c"].add_dir("c")
    tree.children["c"].children["c"].add_file("a", 1000)
    tree.children["c"].children["c"].add_file("b", 1000)
    tree.children["c"].children["c"].add_file("c", 1000)
    return tree
        

if __name__ == "__main__":
    inp = get_input("input.txt")
    tree = create_directory_tree(inp)
    # tree = test_tree()
    print(tree.bf_search(100000))
