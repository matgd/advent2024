from itertools import product
from dataclasses import dataclass
import re

INPUT_FILENAME = "tinput.txt"

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


def part2(equations: list[Equation]):
    operators = ("+", "*", "||")
    possible_desired_results = []
    for equation in equations:
        for op_combination in product(operators, repeat=len(equation.numbers) - 1):
            raw_eq = []
            for i, num in enumerate(equation.numbers):
                raw_eq.append(num)
                if i < len(op_combination):
                    raw_eq.append(op_combination[i])
            raw_eq = "".join(map(str, raw_eq))
            raw_eq = raw_eq.replace("||", "")
            eq = re.split(r"(\d+)", raw_eq)[1:-1]
            print(eq)
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
part2(input)