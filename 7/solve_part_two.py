"""

https://adventofcode.com/2022/day/7#part2

--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""

from typing import Dict


class Dir:
    def __init__(
        self,
        name: str = None,
        size: int = 0,
        parent: "Dir" = None,
        kids: Dict = {},
    ):
        self.name = name
        self.size = size
        self.parent = parent
        self.kids = kids


# save lines of input.txt to a list
with open("input.txt") as f:
    cmd_list = f.read().splitlines()

dir_tree = Dir(name="/", size=0)

iter_tree = dir_tree
cmd_idx = 0


while cmd_idx < len(cmd_list):

    curr_cmd = cmd_list[cmd_idx].strip()
    cmd = curr_cmd.split()
    # print("=" * 30)
    # print(cmd)
    if cmd[1] == "cd":
        if cmd[2] == "..":
            iter_tree = iter_tree.parent
        elif cmd[2] == "/":
            iter_tree = dir_tree
        else:
            if cmd[2] not in iter_tree.kids:
                new_node = Dir(name=cmd[2], size=0, parent=iter_tree, kids={})
                iter_tree.kids[cmd[2]] = new_node
            iter_tree = iter_tree.kids[cmd[2]]
        cmd_idx += 1
    elif cmd[1] == "ls":
        cmd_idx += 1
        while cmd_idx < len(cmd_list) and not cmd_list[cmd_idx].startswith("$"):
            curr_entry = cmd_list[cmd_idx].strip()
            # print(curr_entry)
            if not curr_entry.startswith("dir"):
                file_size = int(curr_entry.split()[0])
                # update tree, by adding the size of current file to the iter_tree and all its parents
                iter_tree.size += file_size
                temp_iter = iter_tree
                while temp_iter.parent:
                    temp_iter.parent.size += file_size
                    temp_iter = temp_iter.parent
            cmd_idx += 1


sum_sizes = 0
root = dir_tree
space_to_free = 30000000 - (70000000 - root.size)

print("space_to_free:", space_to_free)


def find_smallest(node: Dir, space_to_free: int):
    # find the smallest node that has size >= space_to_free
    queue = [node]
    smallest = node.size
    while queue:
        curr_node = queue.pop(0)
        if curr_node.size >= space_to_free and curr_node.size < smallest:
            smallest = curr_node.size
        for kid in curr_node.kids.values():
            queue.append(kid)
    return smallest


print("minimum folder size to free for the update:", find_smallest(root, space_to_free))
