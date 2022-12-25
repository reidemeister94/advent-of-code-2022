"""

https://adventofcode.com/2022/day/24

--- Day 24: Blizzard Basin ---
With everything replanted for next year (and with elephants and monkeys to tend the grove), you and the Elves leave for the extraction point.

Partway up the mountain that shields the grove is a flat, open area that serves as the extraction point. It's a bit of a climb, but nothing the expedition can't handle.

At least, that would normally be true; now that the mountain is covered in snow, things have become more difficult than the Elves are used to.

As the expedition reaches a valley that must be traversed to reach the extraction site, you find that strong, turbulent winds are pushing small blizzards of snow and sharp ice around the valley. It's a good thing everyone packed warm clothes! To make it across safely, you'll need to find a way to avoid them.

Fortunately, it's easy to see all of this from the entrance to the valley, so you make a map of the valley and the blizzards (your puzzle input). For example:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
The walls of the valley are drawn as #; everything else is ground. Clear ground - where there is currently no blizzard - is drawn as .. Otherwise, blizzards are drawn with an arrow indicating their direction of motion: up (^), down (v), left (<), or right (>).

The above map includes two blizzards, one moving right (>) and one moving down (v). In one minute, each blizzard moves one position in the direction it is pointing:

#.#####
#.....#
#.>...#
#.....#
#.....#
#...v.#
#####.#
Due to conservation of blizzard energy, as a blizzard reaches the wall of the valley, a new blizzard forms on the opposite side of the valley moving in the same direction. After another minute, the bottom downward-moving blizzard has been replaced with a new downward-moving blizzard at the top of the valley instead:

#.#####
#...v.#
#..>..#
#.....#
#.....#
#.....#
#####.#
Because blizzards are made of tiny snowflakes, they pass right through each other. After another minute, both blizzards temporarily occupy the same position, marked 2:

#.#####
#.....#
#...2.#
#.....#
#.....#
#.....#
#####.#
After another minute, the situation resolves itself, giving each blizzard back its personal space:

#.#####
#.....#
#....>#
#...v.#
#.....#
#.....#
#####.#
Finally, after yet another minute, the rightward-facing blizzard on the right is replaced with a new one on the left facing the same direction:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
This process repeats at least as long as you are observing it, but probably forever.

Here is a more complex example:

#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
Your expedition begins in the only non-wall position in the top row and needs to reach the only non-wall position in the bottom row. On each minute, you can move up, down, left, or right, or you can wait in place. You and the blizzards act simultaneously, and you cannot share a position with a blizzard.

In the above example, the fastest way to reach your goal requires 18 steps. Drawing the position of the expedition as E, one way to achieve this is:

Initial state:
#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

Minute 1, move down:
#.######
#E>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#

Minute 2, move down:
#.######
#.2>2..#
#E^22^<#
#.>2.^>#
#.>..<.#
######.#

Minute 3, wait:
#.######
#<^<22.#
#E2<.2.#
#><2>..#
#..><..#
######.#

Minute 4, move up:
#.######
#E<..22#
#<<.<..#
#<2.>>.#
#.^22^.#
######.#

Minute 5, move right:
#.######
#2Ev.<>#
#<.<..<#
#.^>^22#
#.2..2.#
######.#

Minute 6, move right:
#.######
#>2E<.<#
#.2v^2<#
#>..>2>#
#<....>#
######.#

Minute 7, move down:
#.######
#.22^2.#
#<vE<2.#
#>>v<>.#
#>....<#
######.#

Minute 8, move left:
#.######
#.<>2^.#
#.E<<.<#
#.22..>#
#.2v^2.#
######.#

Minute 9, move up:
#.######
#<E2>>.#
#.<<.<.#
#>2>2^.#
#.v><^.#
######.#

Minute 10, move right:
#.######
#.2E.>2#
#<2v2^.#
#<>.>2.#
#..<>..#
######.#

Minute 11, wait:
#.######
#2^E^2>#
#<v<.^<#
#..2.>2#
#.<..>.#
######.#

Minute 12, move down:
#.######
#>>.<^<#
#.<E.<<#
#>v.><>#
#<^v^^>#
######.#

Minute 13, move down:
#.######
#.>3.<.#
#<..<<.#
#>2E22.#
#>v..^<#
######.#

Minute 14, move right:
#.######
#.2>2..#
#.^22^<#
#.>2E^>#
#.>..<.#
######.#

Minute 15, move right:
#.######
#<^<22.#
#.2<.2.#
#><2>E.#
#..><..#
######.#

Minute 16, move right:
#.######
#.<..22#
#<<.<..#
#<2.>>E#
#.^22^.#
######.#

Minute 17, move down:
#.######
#2.v.<>#
#<.<..<#
#.^>^22#
#.2..2E#
######.#

Minute 18, move down:
#.######
#>2.<.<#
#.2v^2<#
#>..>2>#
#<....>#
######E#
What is the fewest number of minutes required to avoid the blizzards and reach the goal?

"""

from typing import List, Set
from collections import deque

MIN_STEPS = 500
MATRIX_MEMO = {}


def read_input(input_file: str = "input.txt") -> List:

    matrix = []

    for line in open(input_file):
        line_lst = []
        for elem in line.strip():
            if elem == "#" or elem == ".":
                line_lst.append(elem)
            else:
                line_lst.append([elem])
        matrix.append(line_lst)

    return matrix


def update_cell(matrix: List, new_matrix: List, row: int, col: int) -> List:
    elems = matrix[row][col].copy()
    while elems:
        new_row = row
        new_col = col
        elem = elems.pop()
        if elem == "v":
            new_row += 1
            if matrix[new_row][new_col] == "#":
                new_row = 1
        elif elem == "^":
            new_row -= 1
            if matrix[new_row][new_col] == "#":
                new_row = len(matrix) - 2
        elif elem == "<":
            new_col -= 1
            if matrix[new_row][new_col] == "#":
                new_col = len(matrix[0]) - 2
        elif elem == ">":
            new_col += 1
            if matrix[new_row][new_col] == "#":
                new_col = 1

        if new_matrix[new_row][new_col] == ".":
            new_matrix[new_row][new_col] = [elem]
        else:
            new_matrix[new_row][new_col].append(elem)

    return new_matrix


def update_matrix(matrix: List) -> List:
    new_matrix = [[None for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "#":
                new_matrix[i][j] = "#"
            else:
                new_matrix[i][j] = "."

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != "#" and matrix[i][j] != ".":
                new_matrix = update_cell(matrix.copy(), new_matrix.copy(), i, j)
    return new_matrix


def print_matrix(matrix: List, r, c) -> None:
    for i in range(len(matrix)):
        line = ""
        for j in range(len(matrix[0])):
            if i == r and j == c:
                line += "E"
            else:
                line += (
                    matrix[i][j]
                    if isinstance(matrix[i][j], str)
                    else "[" + "".join(matrix[i][j]) + "]"
                )
        print(line)
    print()


def bfs(matrix: List, row: int = 0, col: int = 1, visited: Set = set()) -> None:
    global MIN_STEPS
    global MATRIX_MEMO

    queue = deque([(row, col, 0)])

    while queue:

        r, c, s = queue.popleft()
        if (r, c, s) in visited:
            continue

        if s > MIN_STEPS:
            continue
        if s in MATRIX_MEMO:
            matrix = MATRIX_MEMO[s]
        else:
            matrix = update_matrix(matrix.copy())
            MATRIX_MEMO[s] = matrix.copy()

        visited.add((r, c, s))

        if r == len(matrix) - 1 and c == len(matrix[0]) - 2:
            MIN_STEPS = min(MIN_STEPS, s)

        for i, j in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if (
                0 <= i < len(matrix)
                and 0 <= j < len(matrix[0])
                and (i, j, s + 1) not in visited
                and matrix[i][j] == "."
            ):
                queue.append((i, j, s + 1))
        if (r, c, s + 1) not in visited and matrix[r][c] == ".":
            queue.append((r, c, s + 1))
    return


def main(input_file: str = "input.txt") -> None:
    matrix = read_input(input_file)

    bfs(
        matrix.copy(),
    )
    print(MIN_STEPS)

if __name__ == "__main__":
    main(input_file="input.txt")
