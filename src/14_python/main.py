import sys
import re
from dataclasses import dataclass
from itertools import batched

FILENAME = sys.argv[1]
with open(FILENAME) as f:
    input = re.findall(r'-?\d+', f.read())

BOUNDS_X = (0, 101)
BOUNDS_Y = (0, 103)

@dataclass
class Robot:
    pos: tuple[int, int]
    v: tuple[int, int]

    def move(self, times=1):
        for _ in range(times):
            self.pos = move_with_teleport(self.pos[0] + self.v[0], self.pos[1] + self.v[1])

def move_with_teleport(x, y):
    new_y, new_x = y, x
    if x < BOUNDS_X[0]:
        new_x = BOUNDS_X[1] + x
    if x > BOUNDS_X[1] - 1:
        new_x = x - BOUNDS_X[1]
    if y < BOUNDS_Y[0]:
        new_y = BOUNDS_Y[1] + y
    if y > BOUNDS_Y[1] - 1:
        new_y = y - BOUNDS_Y[1]
    return new_x, new_y

def print_placement(robots: list[Robot]):
    matrix = [['.' for _ in range(BOUNDS_X[1])] for _ in range(BOUNDS_Y[1])]
    for robot in robots:
        matrix[robot.pos[1]][robot.pos[0]] = '#'

    for row in matrix:
        print(''.join(row))
    print()

def count_in_quadrants(robots: list[Robot]):
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        if robot.pos[0] < (BOUNDS_X[1] / 2) - 1 and robot.pos[1] < (BOUNDS_Y[1] / 2) - 1:
            quadrants[0] += 1
        elif robot.pos[0] > BOUNDS_X[1] / 2 and robot.pos[1] < (BOUNDS_Y[1] / 2) -1:
            quadrants[1] += 1
        elif robot.pos[0] < (BOUNDS_X[1] / 2) - 1 and robot.pos[1] > BOUNDS_Y[1] / 2:
            quadrants[2] += 1
        elif robot.pos[0] > BOUNDS_X[1] / 2 and robot.pos[1] > BOUNDS_Y[1] / 2:
            quadrants[3] += 1
    return quadrants

robots = [Robot(v=(int(vx), int(vy)), pos=(int(px), int(py))) for (px, py, vx, vy) in batched(input, 4)]

print_placement(robots)
for r in robots:
    r.move(int(sys.argv[2]))

print_placement(robots)
safety_factor = 1
for q in count_in_quadrants(robots):
    safety_factor *= q
print("Part 1:", safety_factor)  # 224438715

if len(sys.argv) > 3 and sys.argv[3] == 'save':
    with open('inputprogress.txt', 'w') as f:
        for r in robots:
            f.write(f"p={r.pos[0]},{r.pos[1]} v={r.v[0]},{r.v[1]}\n")
