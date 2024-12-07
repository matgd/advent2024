from itertools import product
from dataclasses import dataclass

INPUT_FILENAME = "input.txt"

@dataclass
class Equation:
    desired_result: int
    numbers: list[int]

def parse_input() -> list[Equation]:
    with open(INPUT_FILENAME) as f:
        input = f.read().splitlines()

    parsed = []
    for line in input:
        desired_result_str, numbers_str = line.split(": ")
        parsed.append(Equation(
            desired_result=int(desired_result_str),
            numbers=[int(num) for num in numbers_str.split(" ")]
        ))
    return parsed

def part1(equations: list[Equation]):
    operators = ("+", "*")
    possible_desired_results = []
    for equation in equations:
        for op_combination in product(operators, repeat=len(equation.numbers) - 1):
            result = equation.numbers[0]
            for i, operator in enumerate(op_combination):
                match operator:
                    case "+":
                        result += equation.numbers[i + 1]
                    case "*":
                        result *= equation.numbers[i + 1]
            if result == equation.desired_result:
                possible_desired_results.append(result)
                break
    print(sum(possible_desired_results))


input = parse_input()
part1(input)