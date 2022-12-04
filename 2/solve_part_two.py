"""

https://adventofcode.com/2022/day/2#part2

--- Part Two ---
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?




"""

opponent_map = {
    "A": "r",
    "B": "p",
    "C": "s",
}

desired_outcome_map = {"X": 0, "Y": 1, "Z": 2}

score_shape_map = {
    "r": 1,
    "p": 2,
    "s": 3,
}

# 0 = lost, 1 = draw, 2 = win
score_outcome_map = {0: 0, 1: 3, 2: 6}


# understand which is my move based on the desired outcome, wins = 2, draw = 1, lost = 0
def understand_my_move(desired_outcome, opponent_move):
    if desired_outcome == 1:
        return opponent_move
    elif desired_outcome == 2:
        if opponent_move == "r":
            return "p"
        elif opponent_move == "p":
            return "s"
        elif opponent_move == "s":
            return "r"
    elif desired_outcome == 0:
        if opponent_move == "r":
            return "s"
        elif opponent_move == "p":
            return "r"
        elif opponent_move == "s":
            return "p"


score = 0
for line in open("input.txt", "r"):
    line = line.strip()
    if line == "":
        continue
    opponent_move, outcome = line.split(" ")
    outcome = desired_outcome_map[outcome]
    opponent_move = opponent_map[opponent_move]
    my_move = understand_my_move(outcome, opponent_move)
    score += score_shape_map[my_move] + score_outcome_map[outcome]

print(score)
