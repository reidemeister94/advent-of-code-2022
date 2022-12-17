"""

https://adventofcode.com/2022/day/14

--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?

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

    return coords


def print_board(rocks_coords: Set[Tuple], balls_coords: Set[Tuple]) -> None:
    max_y = max([coord[1] for coord in rocks_coords])
    max_x = max([coord[0] for coord in rocks_coords])
    min_x = min([coord[0] for coord in rocks_coords])
    for y in range(0, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in rocks_coords:
                row += "#"
            elif (x, y) in balls_coords:
                row += "o"
            else:
                row += "."
        print(row)


def throw_ball(
    rocks_coords: Set[Tuple], balls_coords: Set[Tuple], max_y: int
) -> Union[Set[Tuple], bool]:

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
            if ball_pos[1] >= max_y:
                return balls_coords, True

        # try to move down left
        if (ball_pos[0] - 1, ball_pos[1] + 1) not in rocks_coords and (
            ball_pos[0] - 1,
            ball_pos[1] + 1,
        ) not in balls_coords:
            ball_pos[0] -= 1
            ball_pos[1] += 1
            if ball_pos[1] >= max_y:
                return balls_coords, True
            continue

        # try to move down right
        if (ball_pos[0] + 1, ball_pos[1] + 1) not in rocks_coords and (
            ball_pos[0] + 1,
            ball_pos[1] + 1,
        ) not in balls_coords:
            ball_pos[0] += 1
            ball_pos[1] += 1
            if ball_pos[1] >= max_y:
                return balls_coords, True
            continue

        if ball_pos == start_pos_ball:
            positioned = True
    balls_coords.add(tuple(ball_pos))
    return balls_coords, False


def main(input_file):
    rocks_coords = read_input(input_file)
    # get the max y
    max_y = max([coord[1] for coord in rocks_coords])
    balls_coords = set()
    finished = False
    while not finished:
        balls_coords, finished = throw_ball(rocks_coords, balls_coords, max_y)
    print(len(balls_coords))


if __name__ == "__main__":
    main(input_file="input.txt")
