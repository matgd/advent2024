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
            case _:
                raise ValueError(f"Unexpected value: {f}")
    
    return perimeter, same_label_neighbours


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
part1()
