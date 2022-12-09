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

    def bf_search(self, max_size, min_size):
        def search(dirs, max_size, total=0, closest_min=-1):
            new_dirs = []
            for dir_ in dirs:
                new_dirs += [dir_.children[i] for i in dir_.children]

                size = dir_.size(dir_)
                if size <= max_size:
                    total += size

                if closest_min == -1 and size > min_size:
                    closest_min = size
                elif size > min_size and size < closest_min:
                    closest_min = size

            if not new_dirs:
                return total, closest_min
            total, closest_min = search(new_dirs, max_size, total, closest_min)
            return total, closest_min
        return search([self.children[i] for i in self.children], max_size, min_size)


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
    size, _ = tree.bf_search(100000, -1)
    print(size)

    DISK_TOTAL = 70000000
    MIN_NEEDED = 30000000
    total = tree.size(tree)
    to_free = MIN_NEEDED - (DISK_TOTAL - total)
    _, closest_min = tree.bf_search(1000000, to_free)
    print(closest_min)
