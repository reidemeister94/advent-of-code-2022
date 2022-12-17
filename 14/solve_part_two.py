"""

https://adventofcode.com/2022/day/14#part2

--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?


"""

from typing import Set, Tuple, Union


def read_input(input_file: str = "example.txt") -> Set[Tuple]:

    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    coords = set()
    for i in range(len(lines)):
        curr_line = lines[i].split(" -> ")

        for j in range(len(curr_line) - 1):

            point = curr_line[j].split(",")
            next_point = curr_line[j + 1].split(",")

            x1 = int(point[0])
            x2 = int(next_point[0])
            y1 = int(point[1])
            y2 = int(next_point[1])

            if x1 == x2:
                y = min(y1, y2)
                while y <= max(y1, y2):
                    coords.add((x1, y))
                    y += 1

            elif y1 == y2:
                x = min(x1, x2)
                while x <= max(x1, x2):
                    coords.add((x, y1))
                    x += 1

    max_y = max([coord[1] for coord in coords])
    for i in range(0, 50000):
        coords.add((i, max_y + 2))

    return coords


def print_board(rocks_coords: Set[Tuple], balls_coords: Set[Tuple]) -> None:
    max_y = max([coord[1] for coord in rocks_coords])
    for y in range(0, max_y + 1):
        row = ""
        for x in range(450, 550):
            if (x, y) in rocks_coords:
                row += "#"
            elif (x, y) in balls_coords:
                row += "o"
            else:
                row += "."
        print(row)


def throw_ball(
    rocks_coords: Set[Tuple], balls_coords: Set[Tuple]
) -> Union[Set[Tuple], bool]:

    if (500, 0) in balls_coords:
        return balls_coords, True

    positioned = False
    ball_pos = [500, 0]

    while not positioned:
        start_pos_ball = ball_pos.copy()

        # down
        while (ball_pos[0], ball_pos[1] + 1) not in rocks_coords and (
            ball_pos[0],
            ball_pos[1] + 1,
        ) not in balls_coords:
            ball_pos[1] += 1

        # try to move down left
        if (ball_pos[0] - 1, ball_pos[1] + 1) not in rocks_coords and (
            ball_pos[0] - 1,
            ball_pos[1] + 1,
        ) not in balls_coords:
            ball_pos[0] -= 1
            ball_pos[1] += 1
            continue

        # try to move down right
        if (ball_pos[0] + 1, ball_pos[1] + 1) not in rocks_coords and (
            ball_pos[0] + 1,
            ball_pos[1] + 1,
        ) not in balls_coords:
            ball_pos[0] += 1
            ball_pos[1] += 1
            continue

        if ball_pos == start_pos_ball:
            positioned = True
    balls_coords.add(tuple(ball_pos))
    return balls_coords, False


def main(input_file):
    rocks_coords = read_input(input_file)
    balls_coords = set()
    finished = False
    while not finished:
        balls_coords, finished = throw_ball(rocks_coords, balls_coords)
    print(len(balls_coords))


if __name__ == "__main__":
    main(input_file="input.txt")
