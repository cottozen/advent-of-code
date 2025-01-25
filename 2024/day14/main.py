import math
import functools
import re
from typing import DefaultDict, Literal, NamedTuple


WIDE = 101
TALL = 103
X_MID = WIDE // 2
Y_MID = TALL // 2
SIZE = X_MID * Y_MID
NUM_SECONDS = 100

type Quadrant = Literal["Q1", "Q2", "Q3", "Q4"]


class Robot(NamedTuple):
    x: int
    y: int
    v_x: int
    v_y: int

    def assign_qdrant(self) -> Quadrant | None:
        if self.x < X_MID and self.y < Y_MID:
            return "Q1"
        if self.x > X_MID and self.y < Y_MID:
            return "Q2"
        if self.x > X_MID and self.y > Y_MID:
            return "Q3"
        if self.x < X_MID and self.y > Y_MID:
            return "Q4"
        return None

    def move(self) -> "Robot":
        x = (self.x + self.v_x) % WIDE
        y = (self.y + self.v_y) % TALL
        r = Robot(x, y, self.v_x, self.v_y)
        return r

    def display(self):
        print("=========" * 10)
        print(self)
        for i in range(TALL):
            for j in range(WIDE):
                if j == self.x and i == self.y:
                    print("1", end="")
                else:
                    print(".", end="")
            print()
        print("=========" * 10)


INT_REGEX = r"[-+]?\d+"


def parse_robots(input: str):
    return [
        Robot(x, y, v_x, v_y)
        for x, y, v_x, v_y in map(
            lambda line: map(int, re.findall(INT_REGEX, line)), input.split("\n")
        )
    ]


def display_robots(robots: list[Robot]):
    for i in range(TALL):
        for j in range(WIDE):
            robot_found = False
            for r in robots:
                if j == r.x and i == r.y:
                    robot_found = True
                    break
            if robot_found:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print("=========" * 10)


def calculate_quadrant_entropy(qdrants: dict[Quadrant, int]):
    entropy = 0
    for q in qdrants.values():
        p1 = (SIZE - q) / SIZE
        p2 = q / SIZE
        entropy += p1 * math.log2(1 / p1) + (p2 * math.log2(1 / p2))
    entropy /= 4
    return entropy


def simulate_robots(robots: list[Robot], seconds: int, debug: bool = False):
    min_entropy, min_entropy_second = float("inf"), -1
    for s in range(seconds):
        for i, r in enumerate(robots):
            robots[i] = r.move()
            if debug:
                r.display()
        _, qdrants = assign_robot_quadrant(robots)
        entropy = calculate_quadrant_entropy(qdrants)
        # Checking the entropy reduces the number states we have to consider since most of the robot states are equally random.
        if entropy < min_entropy:
            min_entropy = entropy
            min_entropy_second = s
            print(f"Min entropy at second {min_entropy_second }: ", min_entropy)
            display_robots(robots)


def assign_robot_quadrant(robots: list[Robot]) -> tuple[int, dict[Quadrant, int]]:
    qdrants = DefaultDict(int)
    for r in robots:
        if q := r.assign_qdrant():
            qdrants[q] += 1
    return functools.reduce(lambda a, b: a * b, qdrants.values()), qdrants


def main():
    with open("input.txt") as file:
        robots = parse_robots(file.read().strip())
        simulate_robots(robots, NUM_SECONDS)
        result, _ = assign_robot_quadrant(robots)
        print("RESULT: ", result)
        # Find xmas tree
        simulate_robots(robots, NUM_SECONDS * 100)


if __name__ == "__main__":
    main()
