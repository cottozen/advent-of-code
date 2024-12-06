from typing import Callable


def get_input() -> list[str]:
    file_name = "input.txt"
    with open(file_name, "r") as file:
        return file.readlines()


def is_condition_not_met(x: int, y: int, should_be_ascending: bool) -> bool:
    diff = abs(y - x)
    is_ascending = x > y
    return diff < 1 or diff > 3 or is_ascending is not should_be_ascending


def is_level_safe_default(numbers: list[int]) -> bool:
    # if last element is greater than the first element it must be ascending to be a safe level.
    should_be_ascending = numbers[-1] > numbers[0]
    for i in range(1, len(numbers)):
        if is_condition_not_met(numbers[i], numbers[i - 1], should_be_ascending):
            return False
    return True


def is_level_safe_with_removal(numbers: list[int]) -> bool:
    removal_index = -1
    # O(N*N)
    while removal_index < len(numbers):
        if is_level_safe_default(
            [numbers[i] for i in range(len(numbers)) if i != removal_index]
        ):
            return True
        removal_index += 1
    return False


def find_safe_levels(
    inputs: list[str], is_level_safe: Callable[[list[int]], bool]
) -> list[int]:
    safe_levels = [
        i
        for i, line in enumerate(inputs)
        if is_level_safe([int(n) for n in line.split(" ")])
    ]
    return safe_levels


def test_example_part_2():
    inputs = [
        "7 6 4 2 1",
        "1 2 7 8 9",
        "9 7 6 2 1",
        "1 3 2 4 5",
        "8 6 4 4 1",
    ]
    safe_levels = find_safe_levels(inputs, is_level_safe_with_removal)
    assert safe_levels == [0, 3, 4]


def test_example_part_1():
    inputs = [
        "7 6 4 2 1",
        "1 2 7 8 9",
        "9 7 6 2 1",
        "1 3 2 4 5",
        "8 6 4 4 1",
        "1 3 6 7 9",
    ]
    safe_levels = find_safe_levels(inputs, is_level_safe_default)
    assert safe_levels == [0, 5]


def run_tests():
    test_example_part_1()
    test_example_part_2()


def main():
    inputs = get_input()

    answer_one = len(
        find_safe_levels(inputs=inputs, is_level_safe=is_level_safe_default)
    )
    print("Part one answer is: ", answer_one)
    answer_two = len(
        find_safe_levels(inputs=inputs, is_level_safe=is_level_safe_with_removal)
    )
    print("Part two answer is: ", answer_two)


if __name__ == "__main__":
    run_tests()
    main()
