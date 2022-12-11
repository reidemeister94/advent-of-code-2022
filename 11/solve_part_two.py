"""
https://adventofcode.com/2022/day/11#part2

--- Part Two ---
You're worried you might not ever get your items back. So worried, in fact, that your relief that a monkey's inspection didn't damage an item no longer causes your worry level to be divided by three.

Unfortunately, that relief was all that was keeping your worry levels from reaching ridiculous levels. You'll need to find another way to keep your worry levels manageable.

At this rate, you might be putting up with these monkeys for a very long time - possibly 10000 rounds!

With these new rules, you can still figure out the monkey business after 10000 rounds. Using the same example above:

== After round 1 ==
Monkey 0 inspected items 2 times.
Monkey 1 inspected items 4 times.
Monkey 2 inspected items 3 times.
Monkey 3 inspected items 6 times.

== After round 20 ==
Monkey 0 inspected items 99 times.
Monkey 1 inspected items 97 times.
Monkey 2 inspected items 8 times.
Monkey 3 inspected items 103 times.

== After round 1000 ==
Monkey 0 inspected items 5204 times.
Monkey 1 inspected items 4792 times.
Monkey 2 inspected items 199 times.
Monkey 3 inspected items 5192 times.

== After round 2000 ==
Monkey 0 inspected items 10419 times.
Monkey 1 inspected items 9577 times.
Monkey 2 inspected items 392 times.
Monkey 3 inspected items 10391 times.

== After round 3000 ==
Monkey 0 inspected items 15638 times.
Monkey 1 inspected items 14358 times.
Monkey 2 inspected items 587 times.
Monkey 3 inspected items 15593 times.

== After round 4000 ==
Monkey 0 inspected items 20858 times.
Monkey 1 inspected items 19138 times.
Monkey 2 inspected items 780 times.
Monkey 3 inspected items 20797 times.

== After round 5000 ==
Monkey 0 inspected items 26075 times.
Monkey 1 inspected items 23921 times.
Monkey 2 inspected items 974 times.
Monkey 3 inspected items 26000 times.

== After round 6000 ==
Monkey 0 inspected items 31294 times.
Monkey 1 inspected items 28702 times.
Monkey 2 inspected items 1165 times.
Monkey 3 inspected items 31204 times.

== After round 7000 ==
Monkey 0 inspected items 36508 times.
Monkey 1 inspected items 33488 times.
Monkey 2 inspected items 1360 times.
Monkey 3 inspected items 36400 times.

== After round 8000 ==
Monkey 0 inspected items 41728 times.
Monkey 1 inspected items 38268 times.
Monkey 2 inspected items 1553 times.
Monkey 3 inspected items 41606 times.

== After round 9000 ==
Monkey 0 inspected items 46945 times.
Monkey 1 inspected items 43051 times.
Monkey 2 inspected items 1746 times.
Monkey 3 inspected items 46807 times.

== After round 10000 ==
Monkey 0 inspected items 52166 times.
Monkey 1 inspected items 47830 times.
Monkey 2 inspected items 1938 times.
Monkey 3 inspected items 52013 times.
After 10000 rounds, the two most active monkeys inspected items 52166 and 52013 times. Multiplying these together, the level of monkey business in this situation is now 2713310158.

Worry levels are no longer divided by three after each item is inspected; you'll need to find another way to keep your worry levels manageable. Starting again from the initial state in your puzzle input, what is the level of monkey business after 10000 rounds?


"""
from typing import Dict, List

MOD = 1


class Monkey:
    def __init__(
        self,
        name: int,
        starting_items: List[int],
        operation: str,
        test: int,
        if_true: int,
        if_false: int,
        n_inpections: int = 0,
    ):
        self.name = name
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.n_inspections = n_inpections


def read_input(name_file: str = "input.txt"):

    global MOD

    lines_input = open(name_file, "r").readlines()
    lines_input = [line.strip() for line in lines_input]

    """
    the input is in the format:

    Monkey 0:
    Starting items: 84, 72, 58, 51
    Operation: new = old * 3
    Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 7

    for all the monkeys
    """
    monkeys_data = {}
    for line in lines_input:
        if line.startswith("Monkey"):
            monkey_name = int(line.split()[1].replace(":", "").strip())
            monkeys_data[monkey_name] = {}
        elif line.startswith("Starting items"):
            monkeys_data[monkey_name]["items"] = [
                int(i.strip()) for i in line.split(":")[1].split(",")
            ]
        elif line.startswith("Operation"):
            operation = line.split(":")[1].strip().split("=")[1].split()[1:]
            monkeys_data[monkey_name]["operation"] = {
                "operator": operation[0].strip(),
                "operand": operation[1].strip(),
            }
        elif line.startswith("Test"):
            monkeys_data[monkey_name]["test"] = int(line.split()[-1].strip())
            MOD *= monkeys_data[monkey_name]["test"]
        elif line.startswith("If true"):
            monkeys_data[monkey_name]["if_true"] = int(line.split()[-1].strip())
        elif line.startswith("If false"):
            monkeys_data[monkey_name]["if_false"] = int(line.split()[-1].strip())

    return monkeys_data


def inspect_items(monkeys: Dict[int, Monkey]) -> Dict[int, Monkey]:
    for monkey_name in monkeys:
        monkey = monkeys[monkey_name]
        monkey.n_inspections += len(monkey.items)
        for item in monkey.items:
            item = int(item)
            if monkey.operation["operator"] == "*":
                if monkey.operation["operand"] == "old":
                    new_item = item**2
                else:
                    new_item = item * int(monkey.operation["operand"])
            elif monkey.operation["operator"] == "+":
                if monkey.operation["operand"] == "old":
                    new_item = item * 2
                else:
                    new_item = item + int(monkey.operation["operand"])
            new_item %= MOD
            if new_item % monkey.test == 0:
                monkeys[monkey.if_true].items.append(new_item)
            else:
                monkeys[monkey.if_false].items.append(new_item)
        monkey.items = []
        monkeys[monkey_name] = monkey
    return monkeys


def monkey_business(monkeys_data: Dict, rounds: int = 10000):
    monkeys = {}
    for monkey_name, monkey_data in monkeys_data.items():
        monkeys[monkey_name] = Monkey(
            monkey_name,
            monkey_data["items"],
            monkey_data["operation"],
            monkey_data["test"],
            monkey_data["if_true"],
            monkey_data["if_false"],
        )

    for _ in range(rounds):
        monkeys = inspect_items(monkeys)
    return monkeys


if __name__ == "__main__":

    monkeys_data = read_input()
    monkeys = monkey_business(monkeys_data, rounds=10000)

    # find the two most active monkeys
    most_active_monkeys = sorted(
        monkeys.values(), key=lambda monkey: monkey.n_inspections, reverse=True
    )[:2]
    print(most_active_monkeys[0].n_inspections * most_active_monkeys[1].n_inspections)
