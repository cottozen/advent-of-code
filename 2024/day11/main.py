import functools
import math


def parse_stones(input: str) -> list[int]:
    return [int(c) for c in input.split(" ")]


def split_number(n: int, num_digits: int) -> tuple[int, int]:
    div = 10 ** (num_digits // 2)
    left = n // div
    right = n - (left * div)
    return left, right


def get_digits(n: int) -> int:
    return int(math.log10(n) + 1)


# Cache all results from function
@functools.cache
def get_stones(s: int, num_blinks: int) -> int:
    if num_blinks == 0:
        return 1
    if s == 0:
        return get_stones(1, num_blinks - 1)
    elif (num_digits := get_digits(s)) and num_digits % 2 == 0:
        left, right = split_number(s, num_digits)
        return get_stones(left, num_blinks - 1) + get_stones(right, num_blinks - 1)
    else:
        return get_stones(s * 2024, num_blinks - 1)


def blink(stones: list[int], num_blinks: int):
    return sum([get_stones(s, num_blinks) for s in stones])


def main():
    with open("input.txt") as file:
        stones = parse_stones(file.read())
        num_stones = blink(stones, num_blinks=25)
        print("RESULT: ", num_stones)
        num_stones = blink(stones, num_blinks=75)
        print("RESULT PART TWO: ", num_stones)


if __name__ == "__main__":
    main()
