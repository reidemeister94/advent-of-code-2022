"""
https://adventofcode.com/2022/day/15#part2

--- Part Two ---
Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not detected by any sensor, but the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20. With this reduced search area, there is only a single position that could have a beacon: x=14, y=11. The tuning frequency for this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning frequency?

"""

from typing import List, Set, Union


def read_input(input_file: str = "input.txt") -> Union[List, Set]:
    """Read input file and return a list of integers."""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    devices = set()
    sensors_map = []

    for line in lines:
        line = (
            line.replace(",", "").replace(":", "").replace("x=", "").replace("y=", "")
        )
        coords = line.split(" ")
        sensor = (int(coords[2]), int(coords[3]))
        beacon = (int(coords[8]), int(coords[9]))
        devices.add(sensor)
        devices.add(beacon)
        man_dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        sensors_map.append((sensor[0], sensor[1], man_dist))

    return sensors_map, devices


def main(file_name: str = "input.txt", limit_coord: int = 4_000_000):
    sensors_map, _ = read_input(file_name)

    for target_y in range(limit_coord + 1):
        x_ranges = []
        for s_x, s_y, distance in sensors_map:
            diff_x = distance - abs(target_y - s_y)
            if diff_x >= 0:
                x_ranges.append((s_x - diff_x, s_x + diff_x))

        x_ranges.sort()

        coverage = x_ranges[0]
        for i in range(1, len(x_ranges)):
            if x_ranges[i][0] <= coverage[1]:
                coverage = (coverage[0], max(coverage[1], x_ranges[i][1]))
            else:
                return (coverage[1] + 1) * 4000000 + target_y


if __name__ == "__main__":
    res = main(file_name="input.txt", limit_coord=4_000_000)
    print(res)
