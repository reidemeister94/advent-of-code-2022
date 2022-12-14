"""
https://adventofcode.com/2022/day/12

--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""

from collections import defaultdict, deque
from typing import List

letters_map = {chr(i): i - 97 for i in range(97, 123)}
letters_map["S"] = -1
letters_map["E"] = 26
BEST = float("inf")
N_ROWS = None
N_COLS = None
GRAPH = defaultdict(set)


def read_input(input_file: str = "input.txt") -> List[List[int]]:
    input_lines = open(input_file).read().splitlines()
    input_lines = [list(line.strip()) for line in input_lines]

    heightmap = []
    for line in input_lines:
        heightmap.append([letters_map[letter] for letter in line])
    return heightmap


def create_graph(heightmap: List[List[int]]) -> List[List[int]]:
    global N_ROWS
    global N_COLS
    global GRAPH

    for i in range(N_ROWS):
        for j in range(N_COLS):
            for inc_r, inc_c in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                new_r = i + inc_r
                new_c = j + inc_c

                if (
                    0 <= new_r < N_ROWS
                    and 0 <= new_c < N_COLS
                    and heightmap[new_r][new_c] <= heightmap[i][j] + 1
                ):
                    GRAPH[(i, j)].add((new_r, new_c))


def get_start(heightmap: List[List[int]]) -> tuple:

    global N_ROWS
    global N_COLS

    for i in range(N_ROWS):
        for j in range(N_COLS):
            if heightmap[i][j] == letters_map["S"]:
                return (i, j)


def solve(start: tuple, heightmap: List[List[int]], n_steps: int = 0):

    global N_ROWS
    global N_COLS
    global BEST
    global GRAPH

    queue = deque([(start, n_steps)])
    visited = set()

    while queue:
        curr_pos, n_steps = queue.popleft()
        if curr_pos in visited:
            continue
        visited.add(curr_pos)
        n_steps += 1

        if heightmap[curr_pos[0]][curr_pos[1]] == letters_map["E"]:
            BEST = min(BEST, n_steps)
        else:
            for neighbor in GRAPH[curr_pos]:
                if neighbor not in visited:
                    queue.append((neighbor, n_steps))


def main(input_file: str = "input.txt"):
    global N_ROWS
    global N_COLS
    global BEST
    global VISITED

    heightmap = read_input(input_file)
    N_ROWS = len(heightmap)
    N_COLS = len(heightmap[0])
    VISITED = [[0] * N_COLS for _ in range(N_ROWS)]
    create_graph(heightmap)

    start = get_start(heightmap)

    solve(start=start, heightmap=heightmap, n_steps=0)
    print("MIN STEPS:")
    print(BEST - 1)


if __name__ == "__main__":
    main(input_file="input.txt")
