def get_input(pathname):
    with open(pathname, "r") as f:
        return f.read().splitlines()


def max_calories(data):
    """
    Find the elf carrying the most calories in total
    """
    max_cal = 0
    cur_elf = 0

    for line in data:
        # An empty line means the end of the current elf's inventory.
        # See if the calorie count is higher, store it if it is, then
        # reset the current elf to 0.
        if not line:
            if cur_elf > max_cal:
                max_cal = cur_elf
            cur_elf = 0
        else:
            cur_elf += int(line)
    return max_cal


def top_max_calories(data, number):
    """
    Find the top <number> elves with the most calories
    then return the total number carried by those elves.
    """
    top = [0] * number
    cur_elf = 0

    for line in data:
        if not line:
            try:
                # Get the index of the smallest value in the top list that
                # is less than the current elf's inventory. If there are no
                # values that are less then min() will raise a ValueError and
                # we know there is nothing to do. If we find an index overwrite
                # the value at that index with the current elf's calorie count.
                idx = top.index(min(i for i in top if cur_elf > i))
                top[idx] = cur_elf
            except ValueError:
                pass
            cur_elf = 0
        else:
            cur_elf += int(line)
    return sum(top)


if __name__ == "__main__":
    indata = get_input("input1.txt")
    print(max_calories(indata))
    print(top_max_calories(indata, 3))
