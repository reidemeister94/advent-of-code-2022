"""
https://adventofcode.com/2022/day/13#part2

--- Part Two ---
Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received packets.

The distress signal protocol also requires that you include two additional divider packets:

[[2]]
[[6]]
Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two divider packets - into the correct order.

For the example above, the result of putting the packets in the correct order is:

[]
[[]]
[[[]]]
[1,1,3,1,1]
[1,1,5,1,1]
[[1],[2,3,4]]
[1,[2,[3,[4,[5,6,0]]]],8,9]
[1,[2,[3,[4,[5,6,7]]]],8,9]
[[1],4]
[[2]]
[3]
[[4,4],4,4]
[[4,4],4,4,4]
[[6]]
[7,7,7]
[7,7,7,7]
[[8,7,6]]
[9]
Afterward, locate the divider packets. To find the decoder key for this distress signal, you need to determine the indices of the two divider packets and multiply them together. (The first packet is at index 1, the second packet is at index 2, and so on.) In this example, the divider packets are 10th and 14th, and so the decoder key is 140.

Organize all of the packets into the correct order. What is the decoder key for the distress signal?
"""

from typing import List
import ast


def read_input(input_file: str = "input.txt") -> List[List]:
    """input is like this:
    [1,1,3,1,1]
    [1,1,5,1,1]

    [[1],[2,3,4]]
    [[1],4]

    We have to read each couple of lines and return a list of lists
    """
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip() != ""]

    packets = []
    for i in range(0, len(lines)):
        packets.append(ast.literal_eval(lines[i]))
    return packets


def solve_packet(left: List, right: List) -> bool:
    """Compare two packets and return True if they are in the right order"""
    # print(f"Comparing {left} vs {right}")
    idx = 0
    while idx < len(left) and idx < len(right):
        # print(f"Comparing {left[idx]} vs {right[idx]}")
        if isinstance(left[idx], int) and isinstance(right[idx], int):
            if left[idx] < right[idx]:
                return True
            elif left[idx] == right[idx]:
                idx += 1
                continue
            elif left[idx] > right[idx]:
                return False
        elif isinstance(left[idx], list) and isinstance(right[idx], list):
            return solve_packet(left=left[idx], right=right[idx])
        elif isinstance(left[idx], int) and isinstance(right[idx], list):
            return solve_packet(left=[left[idx]], right=right[idx])
        elif isinstance(left[idx], list) and isinstance(right[idx], int):
            return solve_packet(left=left[idx], right=[right[idx]])
        idx += 1

    # print(f"Idx is at the end of one of the lists: {idx}")

    if idx < len(right) and idx >= len(left):
        return True
    elif idx < len(left) and idx >= len(right):
        return False

    return True


def insertion_sort(list1):

    for i in range(1, len(list1)):

        a = list1[i]
        j = i - 1

        while j >= 0 and solve_packet(a, list1[j]):
            list1[j + 1] = list1[j]
            j -= 1

        list1[j + 1] = a

    return list1


def main(input_file: str = "input.txt") -> int:
    packets = read_input(input_file=input_file)
    packets.extend([[[2]], [[6]]])

    packets = insertion_sort(packets)
    result = 1

    for i in range(len(packets)):
        if packets[i] == [[2]] or packets[i] == [[6]]:
            result *= i + 1

    print(f"The result is {result}")


if __name__ == "__main__":
    main(input_file="input.txt")
