"""
https://adventofcode.com/2022/day/18#part2
--- Part Two ---
Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

What is the exterior surface area of your scanned lava droplet?
"""

from typing import Set, Tuple
from collections import deque

dirs_incr = {(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)}
outside_points = set()
inside_points = set()


def read_input(input_file: str = "input.txt") -> Set[Tuple]:
    points = set()
    for line in open(input_file):
        x, y, z = map(int, line.split(","))
        points.add((x, y, z))
    return points


def is_reachable(point: Tuple, points: Set[Tuple]) -> bool:
    global dirs_incr
    global outside_points
    global inside_points

    if point in outside_points:
        return True
    if point in inside_points:
        return False

    seen = set()
    queue = deque([point])

    while queue:
        x, y, z = queue.popleft()
        if (x, y, z) in seen or (x, y, z) in points:
            continue
        seen.add((x, y, z))
        if len(seen) > 2000:
            for p in seen:
                outside_points.add(p)
            return True
        for x_inc, y_inc, z_inc in dirs_incr:
            queue.append((x + x_inc, y + y_inc, z + z_inc))
    for p in seen:
        inside_points.add(p)
    return False


def main(input_file: str = "input.txt") -> int:
    points = read_input(input_file)
    count_reachable = 0

    for x, y, z in points:
        for x_inc, y_inc, z_inc in dirs_incr:
            if is_reachable((x + x_inc, y + y_inc, z + z_inc), points):
                count_reachable += 1
    print(count_reachable)


if __name__ == "__main__":
    main(input_file="input.txt")
