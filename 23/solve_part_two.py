"""
https://adventofcode.com/2022/day/23#part2

--- Part Two ---
It seems you're on the right track. Finish simulating the process and figure out where the Elves need to go. How many rounds did you save them?

In the example above, the first round where no Elf moved was round 20:

.......#......
....#......#..
..#.....#.....
......#.......
...#....#.#..#
#.............
....#.....#...
..#.....#.....
....#.#....#..
.........#....
....#......#..
.......#......
Figure out where the Elves need to go. What is the number of the first round where no Elf moves?

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
    count_move = 0
    proposals = fill_proposals(matrix, n_rows, n_cols, dirs)
    for (dests, origins) in proposals.items():
        if len(origins) == 1:
            count_move += 1
            dest_r, dest_c = dests
            r, c = origins[0]
            matrix[dest_r][dest_c] = "#"
            matrix[r][c] = "."
    return matrix, count_move


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
    round = 1

    while True:
        matrix, count_move = make_round(matrix.copy(), n_rows, n_cols, dirs.copy())
        if count_move == 0:
            print(round)
            break
        dirs = update_dirs(dirs.copy())
        round += 1


if __name__ == "__main__":
    main(input_file="input.txt")
