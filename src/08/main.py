from dataclasses import dataclass
from copy import deepcopy

FILENAME = "input.txt"

@dataclass
class Location:
    y: int
    x: int
    anthena: str | None
    antinode_of: set[str]

@dataclass
class AnthenaMap:
    locations: list[list[Location]]
    anthenas_locations: dict[str, list[Location]]

    def list_antinodes_locs(self) -> list[Location]:
        return [loc for row in self.locations for loc in row if loc.antinode_of]

    def count_antinodes(self) -> int:
        return len(self.list_antinodes_locs())

    def list_antinodes_locs_p2(self) -> list[Location]:
        to_return = []
        for row in self.locations:
            for loc in row:
                anthena_but_not_alone = len(self.anthenas_locations.get(loc.anthena, set())) > 1
                if loc.antinode_of or anthena_but_not_alone:
                    to_return.append(loc)

        return to_return

    def count_antinodes_p2(self) -> int:
        return len(self.list_antinodes_locs_p2())

def parse_input() -> AnthenaMap:
    with open(FILENAME, "r") as file:
        lines = file.readlines()

    locations = []
    anthenas_locations = {}
    for y, line in enumerate(lines):
        locations.append([])
        for x, char in enumerate(line.strip()):
            location = Location(y, x, None, set())
            if char.isalnum():
                location.anthena = char
                anthenas_locations.setdefault(char, []).append(location)
            locations[y].append(location)
    return AnthenaMap(locations, anthenas_locations)

def calc_antinodes_coords(loc_a: Location, loc_b: Location) -> tuple[tuple[int, int], tuple[int, int]]:
    x_diff = abs(loc_a.x - loc_b.x)
    y_diff = abs(loc_a.y - loc_b.y)

    if loc_a.x < loc_b.x and loc_a.y < loc_b.y:
        return (
            (loc_a.y - y_diff, loc_a.x - x_diff),
            (loc_b.y + y_diff, loc_b.x + x_diff)
        )
    elif loc_a.x < loc_b.x and loc_a.y > loc_b.y:
        return (
            (loc_a.y + y_diff, loc_a.x - x_diff),
            (loc_b.y - y_diff, loc_b.x + x_diff)
        )
    elif loc_a.x > loc_b.x and loc_a.y < loc_b.y:
        return (
            (loc_a.y - y_diff, loc_a.x + x_diff),
            (loc_b.y + y_diff, loc_b.x - x_diff)
        )
    elif loc_a.x > loc_b.x and loc_a.y > loc_b.y:
        return (
            (loc_a.y + y_diff, loc_a.x + x_diff),
            (loc_b.y - y_diff, loc_b.x - x_diff)
        )
    else:
        raise ValueError("In one line")


def part1(input: AnthenaMap) -> None:
    for anthena, locs in input.anthenas_locations.items():
        for i, loc_a in enumerate(locs):
            for loc_b in locs[i+1:]:
                ((ca_y, ca_x), (cb_y, cb_x)) = calc_antinodes_coords(loc_a, loc_b)
                if 0 <= ca_y < len(input.locations) and 0 <= ca_x < len(input.locations[0]):
                    input.locations[ca_y][ca_x].antinode_of.add(anthena)
                if 0 <= cb_y < len(input.locations) and 0 <= cb_x < len(input.locations[0]):
                    input.locations[cb_y][cb_x].antinode_of.add(anthena)

    print("Part 1:", input.count_antinodes())

def calc_antinodes_coords_p2(loc_a: Location, loc_b: Location, bounds_y: int, bounds_x: int) -> list[tuple[int, int]]:
    x_diff = abs(loc_a.x - loc_b.x)
    y_diff = abs(loc_a.y - loc_b.y)

    to_return = []
    if loc_a.x < loc_b.x and loc_a.y < loc_b.y:
        new_loc_ay = loc_a.y - y_diff
        new_loc_ax = loc_a.x - x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay - y_diff
            new_loc_ax = new_loc_ax - x_diff

        new_loc_ay = loc_a.y + y_diff
        new_loc_ax = loc_a.x + x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay + y_diff
            new_loc_ax = new_loc_ax + x_diff

    elif loc_a.x < loc_b.x and loc_a.y > loc_b.y:
        new_loc_ay = loc_a.y + y_diff
        new_loc_ax = loc_a.x - x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay + y_diff
            new_loc_ax = new_loc_ax - x_diff

        new_loc_ay = loc_a.y - y_diff
        new_loc_ax = loc_a.x + x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay - y_diff
            new_loc_ax = new_loc_ax + x_diff

    elif loc_a.x > loc_b.x and loc_a.y < loc_b.y:
        new_loc_ay = loc_a.y - y_diff
        new_loc_ax = loc_a.x + x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay - y_diff
            new_loc_ax = new_loc_ax + x_diff

        new_loc_ay = loc_a.y + y_diff
        new_loc_ax = loc_a.x - x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay + y_diff
            new_loc_ax = new_loc_ax - x_diff

    elif loc_a.x > loc_b.x and loc_a.y > loc_b.y:
        new_loc_ay = loc_a.y + y_diff
        new_loc_ax = loc_a.x + x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay - y_diff
            new_loc_ax = new_loc_ax - x_diff

        new_loc_ay = loc_a.y - y_diff
        new_loc_ax = loc_a.x - x_diff
        while (0 <= new_loc_ay < bounds_y and 0 <= new_loc_ax < bounds_x):
            to_return.append((new_loc_ay, new_loc_ax))
            new_loc_ay = new_loc_ay - y_diff
            new_loc_ax = new_loc_ax - x_diff
    else:
        raise ValueError("In one line")
    return to_return

def part2(input: AnthenaMap) -> None:
    for anthena, locs in input.anthenas_locations.items():
        for i, loc_a in enumerate(locs):
            for loc_b in locs[i+1:]:
                for cy, cx in calc_antinodes_coords_p2(loc_a, loc_b, len(input.locations), len(input.locations[0])):
                    if 0 <= cy < len(input.locations) and 0 <= cx < len(input.locations[0]):
                        input.locations[cy][cx].antinode_of.add(anthena)

    print("Part 2:", input.count_antinodes_p2())

input = parse_input()
input_c = deepcopy(input)
part1(input)  # 249
part2(input_c)  # 905