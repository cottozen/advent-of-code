import re
from typing import NamedTuple, TypedDict


class MachineOption(NamedTuple):
    tokens: int
    x: int
    y: int


class ClawMachine(TypedDict):
    option_a: MachineOption
    option_b: MachineOption
    prize_x: int
    prize_y: int


OPTION_A_TOKEN_COST, OPTION_B_TOKEN_COST = 3, 1
OFFSET = 10000000000000


def parse_input(input: str) -> list[ClawMachine]:
    machine_blocks = input.split("\n\n")
    return [
        {
            "option_a": MachineOption(OPTION_A_TOKEN_COST, a_x, a_y),
            "option_b": MachineOption(OPTION_B_TOKEN_COST, b_x, b_y),
            "prize_x": p_x,
            "prize_y": p_y,
        }
        for a_x, a_y, b_x, b_y, p_x, p_y in map(
            lambda block: map(int, re.findall(r"\d+", block)), machine_blocks
        )
    ]


# Lets use math 4head
def solve_claw_machine_with_math(machine: ClawMachine) -> int:
    P_x, P_y, option_a, option_b = (
        machine["prize_x"],
        machine["prize_y"],
        machine["option_a"],
        machine["option_b"],
    )
    A_x = option_a.x
    A_y = option_a.y
    B_x = option_b.x
    B_y = option_b.y

    # Formula derived with simple algebra. This assumes that we are not dividing by Zero.
    b = (A_x * P_y - A_y * P_x) / (A_x * B_y - A_y * B_x)
    a = (P_x - B_x * b) / A_x

    if b.is_integer() and a.is_integer():
        return int(a * OPTION_A_TOKEN_COST + b * OPTION_B_TOKEN_COST)
    return 0


def solve_all_claw_machines(machines: list[ClawMachine]) -> int:
    result = 0
    for m in machines:
        tokens = solve_claw_machine_with_math(m)
        if tokens:
            result += tokens
    return result


def main():
    with open("input.txt") as file:
        input = file.read()
        machines = parse_input(input)
        result = solve_all_claw_machines(machines)
        print("RESULT: ", result)
        for m in machines:
            m["prize_x"] += OFFSET
            m["prize_y"] += OFFSET
        result = solve_all_claw_machines(machines)
        print("RESULT PART TWO: ", result)


if __name__ == "__main__":
    main()
