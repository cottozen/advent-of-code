from typing import Callable, NamedTuple
import math


class Equation(NamedTuple):
    target: int
    numbers: list[int]


def parse_equations(lines: list[str]):
    equations: list[Equation] = []
    for line in lines:
        parts = line.split(":")
        target, numbers = int(parts[0].strip()), [
            int(n) for n in parts[1].split(" ") if n != ""
        ]
        equations.append(Equation(target, numbers))
    return equations


def concat_numbers(a: int, b: int) -> int:
    # return int(str(n1) + str(n2))
    return a * 10 ** (math.floor(math.log10(b)) + 1) + b


type Operation = Callable[[int, int], int]

OPERATIONS: list[Operation] = [
    lambda y, x: y * x,
    lambda y, x: y + x,
    lambda y, x: concat_numbers(y, x),
]


def solve_equations(equations: list[Equation]):
    def solve(target: int, curr: int, numbers: list[int], p: int):
        if curr > target:
            return False
        if p == len(numbers):
            return curr == target
        for operation in OPERATIONS:
            if solve(target, operation(curr, numbers[p]), numbers, p + 1):
                return True

    return sum(
        [
            e.target if solve(e.target, e.numbers[0], e.numbers, 1) else 0
            for e in equations
        ]
    )


def main():
    with open("input.txt") as file:
        lines = file.readlines()
        equations = parse_equations(lines)
    res = solve_equations(equations)
    print("RESULT IS: ", res)


if __name__ == "__main__":
    main()
