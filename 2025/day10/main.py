from typing import NamedTuple
import z3


class Machine(NamedTuple):
    lights: list[int]
    buttons: list[list[int]]
    target: list[int]


machines = []


def make_bit_map(button: list[int], n: int) -> list[int]:
    map = [0 for _ in range(n)]
    for x in button:
        map[x] = 1
    return map


def parse_machines():
    for line in open(0):
        if not line.strip():
            continue
        parts = line.split(" ")
        lights = [int(c == "#") for c in parts[0][1:-1]]
        target = list(map(int, parts[-1].strip()[1:-1].split(",")))
        buttons = [
            make_bit_map(list(map(int, b[1:-1].split(","))), len(target))
            for b in parts[1:-1]
        ]
        machines.append(Machine(lights, buttons, target))

    return machines


def solve_part_1(machine: Machine):
    s = z3.Optimize()
    num_buttons = len(machine.buttons)

    x = []
    for i in range(num_buttons):
        x_i = z3.Int(f"x_{i}")
        x.append(x_i)
        s.add(x_i >= 0)
        s.add(x_i <= 1)

    # A * x = b and
    target_lights = 0
    for i, light in enumerate(machine.lights):
        if light:
            target_lights |= 1 << len(machine.lights) - 1 - i

    for l_i in range(len(machine.lights)):
        light = machine.lights[l_i]
        state = [x[j] for j in range(num_buttons) if machine.buttons[j][l_i] == 1]
        s.add(z3.Sum(state) % 2 == light)

    s.minimize(z3.Sum(x))

    if s.check() == z3.sat:
        m = s.model()
        return sum(m.eval(x_i).as_long() for x_i in x)
    return -1


def solve_part_2(machine: Machine):
    # does a transpose on list of lists
    A = list(zip(*machine.buttons))
    s = z3.Optimize()
    num_buttons = len(machine.buttons)

    x = []
    for i in range(num_buttons):
        x_i = z3.Int(f"x_{i}")
        x.append(x_i)
        s.add(x_i >= 0)

    # A * x = b and
    for i, row_coeffs in enumerate(A):
        equation = z3.Sum([row_coeffs[j] * x[j] for j in range(num_buttons)])
        s.add(equation == machine.target[i])

    s.minimize(z3.Sum(x))

    if s.check() == z3.sat:
        m = s.model()
        return sum(m.eval(x_i).as_long() for x_i in x)
    return -1


def main():
    machines = parse_machines()
    answer1 = 0
    answer2 = 0
    for m in machines:
        answer1 += solve_part_1(m)
        answer2 += solve_part_2(m)
    print("answer1: ", answer1)
    print("answer2: ", answer2)


main()
