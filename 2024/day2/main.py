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


def is_condition_not_met(x: int, y: int, should_be_ascending: bool) -> bool:
    diff = abs(y - x)
    is_ascending = x > y
    return diff < 1 or diff > 3 or is_ascending is not should_be_ascending


def is_level_safe_with_removal(numbers: list[int]) -> bool:
    # if last element is greater than the first element it must be ascending to be a safe level.
    should_be_ascending = numbers[-1] > numbers[0]
    removed_index = None
    for i in range(1, len(numbers)):
        if i == removed_index:
            pass
        if is_condition_not_met(numbers[i], numbers[i - 1], should_be_ascending):
            return False
    return True


def find_safe_levels(inputs: list[str]) -> list[int]:
    safe_levels = [
        i
        for i, line in enumerate(inputs)
        if is_level_safe([int(n) for n in line.split(" ")])
    ]
    return safe_levels


def test_example():
    inputs = [
        "7 6 4 2 1",  # Safe without removing any level.
        "1 2 7 8 9",  # Unsafe regardless of which level is removed.
        "9 7 6 2 1",  # Unsafe regardless of which level is removed.
        "1 3 2 4 5",  # Safe by removing the second level, 3.
        "8 6 4 4 1",  # Safe by removing the third level, 4.
        "1 3 6 7 9",
    ]  # Safe without removing any level.
    assert find_safe_levels(inputs) == [0, 3, 4, 5]


def main():
    inputs = get_input()
    safe_levels = find_safe_levels(inputs=inputs)
    print("Answer is: ", len(safe_levels))


if __name__ == "__main__":
    main()
