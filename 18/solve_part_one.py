"""

https://adventofcode.com/2022/day/18

--- Day 18: Boiling Boulders ---
You and the elephants finally reach fresh air. You've emerged near the base of a large volcano that seems to be actively erupting! Fortunately, the lava seems to be flowing away from you and toward the ocean.

Bits of lava are still being ejected toward you, so you're sheltering in the cavern exit a little longer. Outside the cave, you can see the lava landing in a pond and hear it loudly hissing as it solidifies.

Depending on the specific compounds in the lava and speed at which it cools, it might be forming obsidian! The cooling rate should be based on the surface area of the lava droplets, so you take a quick scan of a droplet as it flies past you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its resolution is quite low and, as a result, it approximates the shape of the lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that are not immediately connected to another cube. So, if your scan were only two adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered and five sides exposed, a total surface area of 10 sides.

Here's a larger example:

2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
In the above example, after counting up all the sides that aren't connected to another cube, the total surface area is 64.

What is the surface area of your scanned lava droplet?

"""

from typing import List, Set, Tuple


class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


def read_input(input_file: str = "input.txt") -> List[Point]:
    points = []
    for line in open(input_file):
        x, y, z = map(int, line.split(","))
        points.append(Point(x, y, z))
    return points


def create_front_face(point: Point) -> Set[Tuple]:
    # create 4 coordinates for the front face, the point is the up right corner
    face = set()
    face.add((point.x, point.y, point.z))
    face.add((point.x - 1, point.y, point.z))
    face.add((point.x - 1, point.y - 1, point.z))
    face.add((point.x, point.y - 1, point.z))
    return face


def create_up_face(point: Point) -> Set[Tuple]:
    face = set()
    face.add((point.x, point.y, point.z))
    face.add((point.x - 1, point.y, point.z))
    face.add((point.x - 1, point.y, point.z - 1))
    face.add((point.x, point.y, point.z - 1))
    return face


def create_right_face(point: Point) -> Set[Tuple]:
    face = set()
    face.add((point.x, point.y, point.z))
    face.add((point.x, point.y - 1, point.z))
    face.add((point.x, point.y - 1, point.z - 1))
    face.add((point.x, point.y, point.z - 1))
    return face


def create_left_face(point: Point) -> Set[Tuple]:
    face = set()
    face.add((point.x - 1, point.y, point.z))
    face.add((point.x - 1, point.y - 1, point.z))
    face.add((point.x - 1, point.y - 1, point.z - 1))
    face.add((point.x - 1, point.y, point.z - 1))
    return face


def create_down_face(point: Point) -> Set[Tuple]:
    face = set()
    face.add((point.x, point.y - 1, point.z))
    face.add((point.x - 1, point.y - 1, point.z))
    face.add((point.x - 1, point.y - 1, point.z - 1))
    face.add((point.x, point.y - 1, point.z - 1))
    return face


def create_back_face(point: Point) -> Set[Tuple]:
    face = set()
    face.add((point.x, point.y, point.z - 1))
    face.add((point.x - 1, point.y, point.z - 1))
    face.add((point.x - 1, point.y - 1, point.z - 1))
    face.add((point.x, point.y - 1, point.z - 1))
    return face


map_int_fn = {
    0: create_front_face,
    1: create_up_face,
    2: create_right_face,
    3: create_left_face,
    4: create_down_face,
    5: create_back_face,
}


def add_point_faces(point: Point, faces: List[Tuple]) -> List[Set[Tuple]]:
    for i in range(6):
        face = map_int_fn[i](point)
        if face in faces:
            faces.remove(face)
        else:
            faces.append(face)
    return faces


def main(input_file: str = "input.txt") -> int:
    points = read_input(input_file)
    faces = []
    for p in points:
        faces = add_point_faces(point=p, faces=faces)
    print(len(faces))


if __name__ == "__main__":
    main(input_file="input.txt")
