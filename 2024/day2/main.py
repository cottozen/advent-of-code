from typing import Callable


def get_input() -> list[str]:
    file_name = "input.txt"
    with open(file_name, "r") as file:
        return file.readlines()


def is_level_safe(numbers: list[int]) -> bool:
    # if last element is greater than the first element it must be ascending to be a safe level.
    should_be_ascending = numbers[-1] > numbers[0]
    for i in range(1, len(numbers)):
        diff = abs(numbers[i - 1] - numbers[i])
        is_ascending = numbers[i] > numbers[i - 1]
        if diff < 1 or diff > 3 or is_ascending is not should_be_ascending:
            return False
    return True


def find_safe_levels(
    inputs: list[str], parse_numbers: Callable[[str], list[int]]
) -> list[int]:
    safe_levels = [
        i for i, line in enumerate(inputs) if is_level_safe(parse_numbers(line))
    ]
    return safe_levels


def main():
    inputs = get_input()
    safe_levels = find_safe_levels(
        inputs=inputs, parse_numbers=lambda line: [int(n) for n in line.split(" ")]
    )
    print("Answer is: ", len(safe_levels))


if __name__ == "__main__":
    main()
