"""
https://adventofcode.com/2022/day/17#part2  

--- Part Two ---
The elephants are not impressed by your simulation. They demand to know how tall the tower will be after 1000000000000 rocks have stopped! Only then will they feel confident enough to proceed through the cave.

In the example above, the tower would be 1514285714288 units tall!

How tall will the tower be after 1000000000000 rocks have stopped?


"""
from typing import Set, Tuple


def read_input(input_file: str = "input.txt") -> str:
    moves = open(input_file).read().strip()
    return moves


def generate_rock_0(max_height: int) -> Set:
    """Generate a rock of type 0"""
    return set([(i + 2, max_height + 3) for i in range(4)])


def generate_rock_1(max_height: int) -> Set:
    """Generate a rock of type 1"""
    return set(
        [(i + 2, max_height + 4) for i in range(3)]
        + [(3, max_height + i + 3) for i in range(3)]
    )


def generate_rock_2(max_height: int) -> Set:
    """Generate a rock of type 2"""
    return set(
        [(i + 2, max_height + 3) for i in range(3)]
        + [(4, max_height + i + 3) for i in range(3)]
    )


def generate_rock_3(max_height: int) -> Set:
    """Generate a rock of type 3"""
    return set([(2, max_height + i + 3) for i in range(4)])


def generate_rock_4(max_height: int) -> Set:
    """Generate a rock of type 4"""
    return set(
        [(i + 2, max_height + 3) for i in range(2)]
        + [(i + 2, max_height + 4) for i in range(2)]
    )


def generate_rock(rock_type: int, max_height: int) -> Set:
    """Generate a rock of a given type and height"""
    if rock_type == 0:
        """rock = ####"""
        return generate_rock_0(max_height)
    elif rock_type == 1:
        """
        rock =
        .#.
        ###
        .#.
        """
        return generate_rock_1(max_height)
    elif rock_type == 2:
        """
        rock =
        ..#
        ..#
        ###
        """
        return generate_rock_2(max_height)
    elif rock_type == 3:
        """
        rock =
        #
        #
        #
        #
        """
        return generate_rock_3(max_height)
    elif rock_type == 4:
        """
        rock =
        ##
        ##
        """
        return generate_rock_4(max_height)


def move_rock_right(rock: Set) -> Set:
    """Move a rock to the right"""
    return set([(i[0] + 1, i[1]) for i in rock])


def move_rock_left(rock: Set) -> Set:
    """Move a rock to the left"""
    return set([(i[0] - 1, i[1]) for i in rock])


def move_rock_down(rock: Set) -> Set:
    """Move a rock down, return max_height and True if the rock is in final position"""
    return set([(i[0], i[1] - 1) for i in rock])


def compute_distances(rocks: Set) -> Tuple[int]:
    dist = [-30 for _ in range(7)]
    for x, y in rocks:
        dist[x] = max(dist[x], y)

    top = max(dist)
    return tuple([d - top for d in dist])


def main(
    input_file: str = "input.txt", rocks_target: int = 1000000000000, check_loops=True
) -> None:
    moves = read_input(input_file)
    rocks = set([(i, -1) for i in range(7)])
    max_height = 0
    rocks_count = 0
    rock_type = 0
    rock = generate_rock(0, 0)
    move_idx = 0
    state_map = {
        (0, 0, (float("inf"), float("inf"), 3, 3, 3, float("inf"), float("inf"))): (
            max_height,
            rocks_count,
        )
    }
    while rocks_count < rocks_target:
        move = moves[move_idx % len(moves)]
        if move == ">":
            temp = move_rock_right(rock)
        else:
            temp = move_rock_left(rock)
        move_idx += 1
        if all([0 <= i[0] < 7 for i in temp]) and not (temp & rocks):
            rock = temp
        temp = move_rock_down(rock)
        if temp & rocks:
            rocks |= rock
            rocks_count += 1
            max_height = max([i[1] for i in rocks]) + 1
            if rocks_count >= rocks_target:
                break
            rock_type = (rock_type + 1) % 5
            rock = generate_rock(rock_type, max_height)
            if check_loops:
                distances = compute_distances(rocks)
                if (
                    move_idx % len(moves),
                    rock_type,
                    distances,
                ) in state_map:
                    state_data = state_map[
                        (move_idx % len(moves), rock_type, distances)
                    ]
                    prev_max_height = state_data[0]
                    prev_rocks_count = state_data[1]
                    n_rocks_in_cycle = rocks_count - prev_rocks_count
                    height_accumulated_in_cycle = max_height - prev_max_height
                    n_rocks_cycles_to_add = (
                        rocks_target - rocks_count
                    ) // n_rocks_in_cycle
                    total_increase_height = (
                        n_rocks_cycles_to_add * height_accumulated_in_cycle
                    )
                    rocks_count_boosted = (
                        rocks_count + n_rocks_in_cycle * n_rocks_cycles_to_add
                    )
                    return (
                        total_increase_height,
                        rocks_target - rocks_count_boosted + rocks_count,
                    )
                else:
                    state_map[(move_idx % len(moves), rock_type, distances)] = (
                        max_height,
                        rocks_count,
                    )
        else:
            rock = temp
    return max_height


if __name__ == "__main__":
    increase_height, rocks_target = main(input_file="input.txt", check_loops=True)
    max_height = main(
        input_file="input.txt", rocks_target=rocks_target, check_loops=False
    )
    print(increase_height + max_height)
