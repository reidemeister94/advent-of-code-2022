"""
https://adventofcode.com/2022/day/16#part2

--- Part Two ---
You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only 26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26 minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
With the elephant helping, after 26 minutes, the best you could do would release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most pressure you could release?
"""


from functools import lru_cache
import time
from typing import Dict


def read_input(input_file: str = "input.txt") -> Dict:
    lines = open(input_file).readlines()
    lines = [line.strip() for line in lines]

    # line: Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

    valves = {}
    valves_map = {}
    count = 0
    for line in lines:
        line = line.split()
        valves[line[1]] = {
            "flow_rate": int(line[4].replace(";", "").split("=")[1]),
            "tunnels": "".join(line[9:]).split(","),
        }
        if line[1] not in valves_map:
            valves_map[line[1]] = count
            count += 1
    return valves, valves_map


def main(input_file: str = "input.txt"):
    valves, valves_map = read_input(input_file=input_file)

    @lru_cache(maxsize=None)
    def dp(
        current_valve: str = "AA",
        time_left: int = 26,
        status: str = "0" * len(valves),
        elephant=False,
    ):
        if time_left <= 0:
            if elephant:
                return dp(
                    current_valve="AA", time_left=26, status=status, elephant=False
                )
            return 0

        res = 0
        for kid in valves[current_valve]["tunnels"]:
            res = max(
                res,
                dp(
                    current_valve=kid,
                    time_left=time_left - 1,
                    status=status,
                    elephant=elephant,
                ),
            )

        if (
            valves[current_valve]["flow_rate"] > 0
            and status[valves_map[current_valve]] == "0"
            and time_left > 0
        ):

            status = list(status)
            status[valves_map[current_valve]] = "1"
            status = "".join(status)

            time_left -= 1
            pressure_gained = valves[current_valve]["flow_rate"] * (time_left)

            for kid in valves[current_valve]["tunnels"]:
                res = max(
                    res,
                    pressure_gained
                    + dp(
                        current_valve=kid,
                        time_left=time_left - 1,
                        status=status,
                        elephant=elephant,
                    ),
                )
        return res

    return dp(current_valve="AA", time_left=26, status="0" * len(valves), elephant=True)


if __name__ == "__main__":
    print(main(input_file="input.txt"))
