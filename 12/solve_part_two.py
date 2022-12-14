"""
https://adventofcode.com/2022/day/11#part2

--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

"""

from collections import defaultdict, deque
from typing import List

letters_map = {chr(i): i - 97 for i in range(97, 123)}
letters_map["E"] = 26
letters_map["S"] = 0
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


def get_starts(heightmap: List[List[int]]) -> tuple:

    global N_ROWS
    global N_COLS

    starts = []

    for i in range(N_ROWS):
        for j in range(N_COLS):
            if heightmap[i][j] == letters_map["a"]:
                starts.append((i, j))
    return starts


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

    starts = get_starts(heightmap)

    for start in starts:
        solve(start=start, heightmap=heightmap, n_steps=0)
    print("MIN STEPS:")
    print(BEST - 1)


if __name__ == "__main__":
    main(input_file="input.txt")
