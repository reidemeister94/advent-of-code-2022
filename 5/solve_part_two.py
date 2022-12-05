"""

https://adventofcode.com/2022/day/5#part2

--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
"""

## ASSUMPTION: REPLACE SPACE IN THE FIRST PART OF THE INPUT WITH XXX

# IN THIS CASE WE JUST NEED TO KEEP THE MOVING PART OF EACH STACK IN THE SAME ORDER

stacks = [[] for _ in range(9)]

for line in open("matrix.txt", "r"):
    elements = line.strip().split(" ")
    elements = [elem.replace("[", "").replace("]", "") for elem in elements]

    for i in range(len(elements)):
        if elements[i] != "XXX":
            stacks[i].append(elements[i])

for i in range(len(stacks)):
    stacks[i] = stacks[i][::-1]


# read moves input: example = move 3 from 1 to 7


for line in open("input.txt", "r"):
    elements = line.strip().split(" ")
    n = int(elements[1])
    from_stack = int(elements[3]) - 1
    to_stack = int(elements[5]) - 1

    stacks[to_stack] += stacks[from_stack][-n:]
    del stacks[from_stack][-n:]


# get last element of each stack
result = ""
for stack in stacks:
    result += stack[-1]

print(result)
