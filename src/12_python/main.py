import sys

FILENAME = sys.argv[1]
with open(FILENAME) as f:
    input = f.read().splitlines()


def field_info(desired_label: str, y: int, x: int):
    if y < 0 or y >= len(input) or x < 0 or x >= len(input[y]):
        return 1

    field = input[y][x]
    if field == desired_label:
        return (y, x)
    else:
        return 1

def get_perimeter_and_neighbours(y: int, x: int) -> tuple[int, list[tuple[int, int]]]:
    region_label = input[y][x]
    top = field_info(region_label, y-1, x)
    left = field_info(region_label, y, x-1)
    right = field_info(region_label, y, x+1)
    bottom = field_info(region_label, y+1, x)

    fields = [top, left, right, bottom]
    same_label_neighbours = []
    perimeter = 0

    for f in fields:
        match f:
            case 1:
                perimeter += 1
            case (y, x):
                same_label_neighbours.append((y, x))
    
    return perimeter, same_label_neighbours

def get_perimeter_coords_and_neighbours(y: int, x: int) -> tuple[set[tuple[int, int]], list[tuple[int, int]]]:
    region_label = input[y][x]
    top = (field_info(region_label, y-1, x), (y-1, x, "top"))
    left = (field_info(region_label, y, x-1), (y, x-1, "left"))
    right = (field_info(region_label, y, x+1), (y, x+1, "right"))
    bottom = (field_info(region_label, y+1, x), (y+1, x, "bottom"))

    fields = [top, left, right, bottom]
    same_label_neighbours = []
    perimeter_coords = set()

    for (f, c) in fields:
        match f:
            case 1:
                perimeter_coords.add(c)
            case (y, x):
                same_label_neighbours.append((y, x))
    
    return perimeter_coords, same_label_neighbours


def part1():
    already_inspected_coords = set()
    regions = []
    for y in range(len(input)):
        for x in range(len(input[y])):
            if (y, x) in already_inspected_coords:
                continue

            region_scrap = [(y, x)]
            perimeter = 0
            region_size = 0
            while region_scrap:
                ry, rx = region_scrap.pop(0)
                if (ry, rx) in already_inspected_coords:
                    continue
                p, n = get_perimeter_and_neighbours(ry, rx)
                perimeter += p
                region_size += 1
                already_inspected_coords.add((ry, rx))
                region_scrap.extend([coord for coord in n if coord not in already_inspected_coords])

            regions.append((region_size, perimeter))
    
    cost = 0
    for rs, p in regions:
        cost += rs * p
    print("Part 1:", cost)

def wall_count(p_coords: list[tuple[int, int, str]]) -> int:
    walls = 0
    coords_bottom = sorted([p for p in p_coords if p[2] == "bottom"])
    coords_top = sorted([p for p in p_coords if p[2] == "top"])
    coords_left = sorted([p for p in p_coords if p[2] == "left"], key=lambda x: (x[1], x[0]))
    coords_right = sorted([p for p in p_coords if p[2] == "right"], key=lambda x: (x[1], x[0]))

    walls = 0
    for dir in [coords_bottom, coords_top]:
        prev_y, prev_x = -99, -99

        for y, x, _ in dir:
            if y != prev_y or x != prev_x + 1:
                walls += 1
            prev_y, prev_x = y, x
            
    for dir in [coords_left, coords_right]:
        prev_y, prev_x = -99, -99

        for y, x, _ in dir:
            if x != prev_x or y != prev_y + 1:
                walls += 1
            prev_y, prev_x = y, x
    return walls


def part2():
    already_inspected_coords = set()
    regions = []
    for y in range(len(input)):
        for x in range(len(input[y])):
            if (y, x) in already_inspected_coords:
                continue

            region_scrap = [(y, x)]
            region_size = 0
            per_coords = []
            while region_scrap:
                ry, rx = region_scrap.pop(0)
                if (ry, rx) in already_inspected_coords:
                    continue
                pc, n = get_perimeter_coords_and_neighbours(ry, rx)
                region_size += 1
                per_coords.extend(pc)
                already_inspected_coords.add((ry, rx))
                region_scrap.extend([coord for coord in n if coord not in already_inspected_coords])

            regions.append((region_size, per_coords))
    
        
    cost = 0
    for rs, p_coords in regions:
        cost += rs * wall_count(p_coords)
    print("Part 2:", cost) 

part1()  # 1377008
part2()  # 815788
