"""
https://adventofcode.com/2022/day/24#part2

--- Part Two ---
As the expedition reaches the far side of the valley, one of the Elves looks especially dismayed:

He forgot his snacks at the entrance to the valley!

Since you're so good at dodging blizzards, the Elves humbly request that you go back for his snacks. From the same initial conditions, how quickly can you make it from the start to the goal, then back to the start, then back to the goal?

In the above example, the first trip to the goal takes 18 minutes, the trip back to the start takes 23 minutes, and the trip back to the goal again takes 13 minutes, for a total time of 54 minutes.

What is the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again?

"""


from typing import List, Set, Tuple
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


def bfs(
    matrix: List,
    end_r: int,
    end_c: int,
    row: int = 0,
    col: int = 1,
    visited: Set = set(),
    minutes: int = 0,
) -> Tuple[List, int]:

    global MATRIX_MEMO

    queue = deque([(row, col, 0)])
    min_steps = 750

    while queue:

        r, c, s = queue.popleft()
        if (r, c, s) in visited:
            continue

        if s > min_steps:
            continue
        if s + minutes in MATRIX_MEMO:
            matrix = MATRIX_MEMO[s + minutes]
        else:
            matrix = update_matrix(matrix.copy())
            MATRIX_MEMO[s + minutes] = matrix.copy()

        visited.add((r, c, s))

        if r == end_r and c == end_c:
            min_steps = min(min_steps, s)

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
    return matrix, min_steps


def main(input_file: str = "input.txt") -> None:
    matrix = read_input(input_file)

    matrix, min_steps_1 = bfs(
        matrix=matrix.copy(),
        end_r=len(matrix) - 1,
        end_c=len(matrix[0]) - 2,
        visited=set(),
    )
    print("first trip to the goal takes", min_steps_1, "minutes")
    # print_matrix(matrix, len(matrix) - 1, len(matrix[0]) - 2)

    matrix, min_steps_2 = bfs(
        matrix=matrix.copy(),
        row=len(matrix) - 1,
        col=len(matrix[0]) - 2,
        end_r=0,
        end_c=1,
        minutes=min_steps_1,
        visited=set(),
    )
    print("second trip to the goal takes", min_steps_2, "minutes")
    # print_matrix(matrix, 0, 1)

    matrix, min_steps_3 = bfs(
        matrix=matrix.copy(),
        end_r=len(matrix) - 1,
        end_c=len(matrix[0]) - 2,
        minutes=min_steps_1 + min_steps_2,
        visited=set(),
    )
    print("last trip to the goal takes", min_steps_3, "minutes")
    # print_matrix(matrix, len(matrix) - 1, len(matrix[0]) - 2)

    print("total time:", min_steps_1 + min_steps_2 + min_steps_3)


if __name__ == "__main__":
    main(input_file="input.txt")
