import heapq
from typing import DefaultDict


def get_input() -> list[str]:
    file_name = "input.txt"
    with open(file_name, "r") as file:
        return file.readlines()


def calculate_sum(left: list[int], right: list[int]):
    total_sum = 0
    for _ in range(len(left)):
        left_min = heapq.heappop(left)
        right_min = heapq.heappop(right)
        total_sum += abs(left_min - right_min)
    return total_sum


def calculate_score(left: list[int], right_counter: DefaultDict[int, int]) -> int:
    total_score = 0
    for v in left:
        total_score += v * right_counter[v]
    return total_score


def main():
    inputs = get_input()
    left: list[int] = []
    right: list[int] = []
    right_counter = DefaultDict(int)
    for line in inputs:
        # Could be more efficent
        values = line.strip().split(" ")
        l_value = int(values[0])
        r_value = int(values[-1])
        right_counter[r_value] += 1
        heapq.heappush(left, l_value)
        heapq.heappush(right, r_value)
    # calculate score first because when summing we are popping from the heap
    score_answer = calculate_score(left, right_counter)
    sum_answer = calculate_sum(left, right)
    print("Sum Answer is: ", sum_answer)
    print("Score Answer is: ", score_answer)


if __name__ == "__main__":
    main()
