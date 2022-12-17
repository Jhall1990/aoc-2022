def get_input(filename):
    with open(filename) as inp:
        return [eval(i.strip()) for i in inp.readlines() if i.strip()]


def get_val(thing, idx):
    """
    Get the value in thing at index. Returns the following info
    <the_value_at_idx>
    """
    try:
        return thing[idx]
    except IndexError:
        return None


def both_ints(left, right):
    return isinstance(left, int) and isinstance(right, int)


def both_lists(left, right):
    return isinstance(left, list) and isinstance(right, list)


def convert_single_item(val):
    return [val] if isinstance(val, int) else val


class Packet():
    def __init__(self, content):
        self.content = content

    def __lt__(self, other):
        """
        Sort just needs __lt__ defined, which is what packet_in_order()
        determines.
        """
        return packet_in_order(self.content, other.content)


def packet_in_order(left, right):
    """
    This function says if two packets are in order based on a bunch
    of arbitrary criteria.
    """
    idx = 0
    while True:
        left_val = get_val(left, idx)
        right_val = get_val(right, idx)
        idx += 1

        if left_val is None and right_val is None:
            return
        elif left_val is None:
            return True
        elif right_val is None:
            return False

        if both_ints(left_val, right_val):
            if left_val == right_val:
                continue
            elif left_val < right_val:
                return True
            return False

        left_val = convert_single_item(left_val)
        right_val = convert_single_item(right_val)

        if both_lists(left_val, right_val):
            result = packet_in_order(left_val, right_val)
            if result is not None:
                return result


def packets_in_order(inp):
    in_order = 0
    for pkt, i in enumerate(range(0, len(inp), 2)):
        if packet_in_order(inp[i], inp[i+1]):
            in_order += pkt + 1
    return in_order


def create_and_sort_packets(inp):
    dividers = ([[2]], [[6]])
    packets = []

    for line in inp:
        packets.append(Packet(line))
    for div in dividers:
        packets.append(Packet(div))

    packets.sort()

    decoder = 1
    for idx, pkt in enumerate(packets):
        for div in dividers:
            if pkt.content == div:
                decoder *= idx + 1
    return decoder


if __name__ == "__main__":
    inp = get_input("input.txt")
    print(packets_in_order(inp))
    print(create_and_sort_packets(inp))
