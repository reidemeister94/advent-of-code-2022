"""

https://adventofcode.com/2022/day/17

--- Day 17: Pyroclastic Flow ---
Your handheld device has located an alternative exit from the cave for you and the elephants. The ground is rumbling almost continuously now, but the strange valves bought you some time. It's definitely getting warmer in here, though.

The tunnels eventually open into a very tall, narrow chamber. Large, oddly-shaped rocks are falling into the chamber from above, presumably due to all the rumbling. If you can't work out where the rocks will fall next, you might be crushed!

The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:

####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
The rocks fall in the order shown above: first the - shape, then the + shape, and so on. Once the end of the list is reached, the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.

The rocks don't spin, but they do get pushed around by jets of hot gas coming out of the walls themselves. A quick scan reveals the effect the jets of hot gas will have on the rocks as they fall (your puzzle input).

For example, suppose this was the jet pattern in your cave:

>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
In jet patterns, < means a push to the left, while > means a push to the right. The pattern above means that the jets will push a falling rock right, then right, then right, then left, then left, then right, and so on. If the end of the list is reached, it repeats.

The tall, vertical chamber is exactly seven units wide. Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).

After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the direction indicated by the next symbol in the jet pattern) and then falling one unit down. If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, the movement instead does not occur. If a downward movement would have caused a falling rock to move into the floor or an already-fallen rock, the falling rock stops where it is (having landed on something) and a new rock immediately begins falling.

Drawing falling rocks with @ and stopped rocks with #, the jet pattern in the example above manifests as follows:

The first rock begins falling:
|..@@@@.|
|.......|
|.......|
|.......|
+-------+

Jet of gas pushes rock right:
|...@@@@|
|.......|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
+-------+

Jet of gas pushes rock left:
|..@@@@.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|..####.|
+-------+

A new rock begins falling:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|...@...|
|..@@@..|
|...@...|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|..####.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

A new rock begins falling:
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+
The moment each of the next few rocks begins falling, you would see this:

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|..#....|
|..#....|
|####...|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|..#....|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|.....#.|
|.....#.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|....##.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+
To prove to the elephants your simulation is accurate, they want to know how tall the tower will get after 2022 rocks have stopped (but before the 2023rd rock begins falling). In this example, the tower of rocks will be 3068 units tall.

How many units tall will the tower of rocks be after 2022 rocks have stopped falling?

"""

"""
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

from typing import Set


def read_input(input_file: str = "input.txt") -> str:
    moves = open(input_file).read().strip()
    return moves


def print_map(rocks: Set, rock: Set, max_height: int) -> None:
    for i in range(max_height + 10, -1, -1):
        line = ""
        for j in range(7):
            if (j, i) in rock:
                line += "@"
            elif (j, i) in rocks:
                line += "#"
            else:
                line += "."
        print(line)


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


def main(input_file: str = "input.txt") -> None:

    moves = read_input(input_file)
    rocks = set([(i, -1) for i in range(7)])
    max_height = 0
    rocks_count = 0
    rock_type = 0
    rock = generate_rock(0, 0)
    move_idx = 0
    while rocks_count < 85:
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
            if rocks_count >= 85:
                break
            rock_type = (rock_type + 1) % 5
            rock = generate_rock(rock_type, max_height)
        else:
            rock = temp
    print(max_height)


if __name__ == "__main__":
    main(input_file="example.txt")
