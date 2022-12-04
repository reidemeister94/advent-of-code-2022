"""
https://adventofcode.com/2022/day/1#part2

--- Part Two ---
By the time you calculate the answer to the Elves' question, 
they've already realized that the Elf carrying the most Calories of food might 
eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total 
Calories carried by the top three Elves carrying the most Calories. 
That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories), 
then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories). 
The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

"""
from collections import defaultdict

calories_map = defaultdict(int)
idx_elf = 0
temp_count = 0
# for each line of input.txt file
for line in open("input.txt", "r"):
    line = line.strip()
    if not line:
        calories_map[idx_elf] += temp_count
        idx_elf += 1
        temp_count = 0
    else:
        temp_count += int(line)


# get the sum of top 3 highest calorie
top_3 = sorted(calories_map.values(), reverse=True)[:3]
print(sum(top_3))
