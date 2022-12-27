"""

https://adventofcode.com/2022/day/23

--- Day 23: Unstable Diffusion ---
You enter a large crater of gray dirt where the grove is supposed to be. All around you, plants you imagine were expected to be full of fruit are instead withered and broken. A large group of Elves has formed in the middle of the grove.

"...but this volcano has been dormant for months. Without ash, the fruit can't grow!"

You look up to see a massive, snow-capped mountain towering above you.

"It's not like there are other active volcanoes here; we've looked everywhere."

"But our scanners show active magma flows; clearly it's going somewhere."

They finally notice you at the edge of the grove, your pack almost overflowing from the random star fruit you've been collecting. Behind you, elephants and monkeys explore the grove, looking concerned. Then, the Elves recognize the ash cloud slowly spreading above your recent detour.

"Why do you--" "How is--" "Did you just--"

Before any of them can form a complete question, another Elf speaks up: "Okay, new plan. We have almost enough fruit already, and ash from the plume should spread here eventually. If we quickly plant new seedlings now, we can still make it to the extraction point. Spread out!"

The Elves each reach into their pack and pull out a tiny plant. The plants rely on important nutrients from the ash, so they can't be planted too close together.

There isn't enough time to let the Elves figure out where to plant the seedlings themselves; you quickly scan the grove (your puzzle input) and note their positions.

For example:

....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
The scan shows Elves # and empty ground .; outside your scan, more empty ground extends a long way in every direction. The scan is oriented so that north is up; orthogonal directions are written N (north), S (south), W (west), and E (east), while diagonal directions are written NE, NW, SE, SW.

The Elves follow a time-consuming process to figure out where they should each go; you can speed up this process considerably. The process consists of some number of rounds during which Elves alternate between considering where to move and actually moving.

During the first half of each round, each Elf considers the eight positions adjacent to themself. If no other Elves are in one of those eight positions, the Elf does not do anything during this round. Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:

If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
After each Elf has had a chance to propose a move, the second half of the round can begin. Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position. If two or more Elves propose moving to the same position, none of those Elves move.

Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list of directions. For example, during the second round, the Elves would try proposing a move to the south first, then west, then east, then north. On the third round, the Elves would first consider west, then east, then north, then south.

As a smaller example, consider just these five Elves:

.....
..##.
..#..
.....
..##.
.....
The northernmost two Elves and southernmost two Elves all propose moving north, while the middle Elf cannot move north and proposes moving south. The middle Elf proposes the same destination as the southwest Elf, so neither of them move, but the other three do:

..##.
.....
..#..
...#.
..#..
.....
Next, the northernmost two Elves and the southernmost Elf all propose moving south. Of the remaining middle two Elves, the west one cannot move south and proposes moving west, while the east one cannot move south or west and proposes moving east. All five Elves succeed in moving to their proposed positions:

.....
..##.
.#...
....#
.....
..#..
Finally, the southernmost two Elves choose not to move at all. Of the remaining three Elves, the west one proposes moving west, the east one proposes moving east, and the middle one proposes moving north; all three succeed in moving:

..#..
....#
#....
....#
.....
..#..
At this point, no Elves need to move, and so the process ends.

The larger example above proceeds as follows:

== Initial State ==
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............

== End of Round 1 ==
..............
.......#......
.....#...#....
...#..#.#.....
.......#..#...
....#.#.##....
..#..#.#......
..#.#.#.##....
..............
....#..#......
..............
..............

== End of Round 2 ==
..............
.......#......
....#.....#...
...#..#.#.....
.......#...#..
...#..#.#.....
.#...#.#.#....
..............
..#.#.#.##....
....#..#......
..............
..............

== End of Round 3 ==
..............
.......#......
.....#....#...
..#..#...#....
.......#...#..
...#..#.#.....
.#..#.....#...
.......##.....
..##.#....#...
...#..........
.......#......
..............

== End of Round 4 ==
..............
.......#......
......#....#..
..#...##......
...#.....#.#..
.........#....
.#...###..#...
..#......#....
....##....#...
....#.........
.......#......
..............

== End of Round 5 ==
.......#......
..............
..#..#.....#..
.........#....
......##...#..
.#.#.####.....
...........#..
....##..#.....
..#...........
..........#...
....#..#......
..............
After a few more rounds...

== End of Round 10 ==
.......#......
...........#..
..#.#..#......
......#.......
...#.....#..#.
.#......##....
.....##.......
..#........#..
....#.#..#....
..............
....#..#..#...
..............
To make sure they're on the right track, the Elves like to check after round 10 that they're making good progress toward covering enough ground. To do this, count the number of empty ground tiles contained by the smallest rectangle that contains every Elf. (The edges of the rectangle should be aligned to the N/S/E/W directions; the Elves do not have the patience to calculate arbitrary rectangles.) In the above example, that rectangle is:

......#.....
..........#.
.#.#..#.....
.....#......
..#.....#..#
#......##...
....##......
.#........#.
...#.#..#...
............
...#..#..#..
In this region, the number of empty ground tiles is 110.

Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds. How many empty ground tiles does that rectangle contain?


"""


from collections import defaultdict, deque
from typing import Dict, List, Tuple

DIRS_COORDS = {
    "N": {(-1, 0), (-1, 1), (-1, -1)},
    "S": {(1, 0), (1, 1), (1, -1)},
    "W": {(0, -1), (-1, -1), (1, -1)},
    "E": {(0, 1), (-1, 1), (1, 1)},
}
DIRS_MAP = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}


def read_input(input_file: str = "input.txt") -> List[List[str]]:
    matrix = [["." for _ in range(200)] for _ in range(200)]
    offset_r = 63
    offset_c = 63
    for line in open(input_file):
        line = line.strip()
        line_lst = []
        for elem in line:
            line_lst.append(elem)
        matrix[offset_r][offset_c : offset_c + len(line_lst)] = line_lst
        offset_r += 1
    return matrix


def is_near_elves(matrix: List[List[str]], i: int, j: int) -> bool:
    for inc_r, inc_c in [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]:
        new_r = i + inc_r
        new_c = j + inc_c
        if (
            0 <= new_r < len(matrix)
            and 0 <= new_c < len(matrix[0])
            and matrix[new_r][new_c] == "#"
        ):
            return True
    return False


def valid_direction(
    matrix: List[List[str]],
    dir: str,
    i: int,
    j: int,
    n_rows: int,
    n_cols: int,
) -> bool:
    global DIRS_COORDS
    global DIRS_MAP
    valid_count = 0
    for inc_r, inc_c in DIRS_COORDS[dir]:
        new_r = i + inc_r
        new_c = j + inc_c
        if 0 <= new_r < n_rows and 0 <= new_c < n_cols and matrix[new_r][new_c] == ".":
            valid_count += 1
    return True if valid_count == 3 else False


def fill_proposals(
    matrix: List[List[str]], n_rows: int, n_cols: int, dirs: List[str]
) -> Dict:
    global DIRS_MAP
    global DIRS_COORDS
    proposals = defaultdict(list)

    for i in range(n_rows):
        for j in range(n_cols):
            if matrix[i][j] == "#":
                if not is_near_elves(matrix.copy(), i, j):
                    continue
                for dir in dirs:
                    if valid_direction(matrix.copy(), dir, i, j, n_rows, n_cols):
                        dest_r = i + DIRS_MAP[dir][0]
                        dest_c = j + DIRS_MAP[dir][1]
                        proposals[(dest_r, dest_c)].append((i, j))
                        break
    return proposals


def make_round(
    matrix: List[List[str]], n_rows: int, n_cols: int, dirs: List[str]
) -> List[List[str]]:
    proposals = fill_proposals(matrix, n_rows, n_cols, dirs)
    for (dests, origins) in proposals.items():
        if len(origins) == 1:
            dest_r, dest_c = dests
            r, c = origins[0]
            matrix[dest_r][dest_c] = "#"
            matrix[r][c] = "."
    return matrix


def update_dirs(dirs: deque) -> deque:
    elem = dirs.popleft()
    dirs.append(elem)
    return dirs


def print_matrix(matrix: List[List[str]]) -> None:
    for i in range(len(matrix)):
        line = ""
        for j in range(len(matrix[0])):
            line += matrix[i][j]
        print(line)
    print()


def get_bounding_box(matrix: List[List[str]]) -> Tuple[int, int, int, int]:
    min_r = float("inf")
    max_r = -1
    min_c = float("inf")
    max_c = -1
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "#":
                min_r = min(min_r, i)
                max_r = max(max_r, i)
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    return min_r, max_r, min_c, max_c


def count_empty_ground_tiles(
    matrix: List[List[str]], min_r: int, min_c: int, max_r: int, max_c: int
) -> int:
    count = 0
    for i in range(min_r, max_r + 1):
        for j in range(min_c, max_c + 1):
            if matrix[i][j] == ".":
                count += 1
    return count


def main(input_file: str = "input.txt") -> None:
    dirs = deque(["N", "S", "W", "E"])
    matrix = read_input(input_file)
    n_rows = len(matrix)
    n_cols = len(matrix[0])

    for _ in range(10):
        matrix = make_round(matrix.copy(), n_rows, n_cols, dirs.copy())
        dirs = update_dirs(dirs.copy())

    min_r, max_r, min_c, max_c = get_bounding_box(matrix.copy())
    print(count_empty_ground_tiles(matrix.copy(), min_r, min_c, max_r, max_c))


if __name__ == "__main__":
    main(input_file="input.txt")
