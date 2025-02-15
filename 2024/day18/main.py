from collections import deque
from typing import Literal, NamedTuple


MAX_X = 70
MAX_Y = 70
NUM_BYTES = 1024
FILE_NAME = "input.txt"


class BytePos(NamedTuple):
    x: int
    y: int


def parse_input():
    byte_positions: list[BytePos] = []
    with open(FILE_NAME, "r") as file:
        for line in file.readlines():
            x, y = line.split(",")
            byte_positions.append(BytePos(int(x), int(y)))
    return byte_positions


type SafeMemory = Literal["."]
type CorruptedMemory = Literal["#"]
type Path = Literal["O"]

type MemorySpace = list[list[SafeMemory | CorruptedMemory | Path]]


def create_memory_space(byte_positions: list[BytePos], num_bytes: int):
    memory: MemorySpace = [["." for _ in range(MAX_X + 1)] for _ in range(MAX_Y + 1)]
    for b_pos in byte_positions[: min(num_bytes, len(byte_positions))]:
        memory[b_pos.y][b_pos.x] = "#"
    return memory


def display_memory_space(memory: MemorySpace):
    for row in memory:
        print("".join(row))


def find_shortest_path(memory: MemorySpace, start: BytePos, target: BytePos):

    visited: set[BytePos] = {start}
    q: deque[BytePos] = deque([start])
    prev: dict[BytePos, BytePos] = {}
    current = 0
    while current >= 0:
        curr = q.popleft()
        if curr == target:
            break
        current -= 1
        neighbours = [
            BytePos(curr.x - 1, curr.y),
            BytePos(curr.x, curr.y - 1),
            BytePos(curr.x + 1, curr.y),
            BytePos(curr.x, curr.y + 1),
        ]
        for n in neighbours:
            if (
                n.x >= 0
                and n.y >= 0
                and n.x <= MAX_X
                and n.y <= MAX_Y
                and memory[n.y][n.x] != "#"
                and n not in visited
            ):
                visited.add(n)
                prev[n] = curr
                q.append(n)
        if current == -1:
            current = len(q) - 1
    curr = target
    path: set[BytePos] = set()
    while p := prev.get(curr):
        path.add(curr)
        curr = p
    return path


def solve_part_two(byte_positions: list[BytePos]):
    start = BytePos(0, 0)
    target = BytePos(MAX_X, MAX_Y)
    memory: MemorySpace = [["." for _ in range(MAX_X + 1)] for _ in range(MAX_Y + 1)]
    curr_path = find_shortest_path(memory, start, target)
    for byte_pos in byte_positions:
        memory[byte_pos.y][byte_pos.x] = "#"
        if byte_pos not in curr_path:
            continue
        curr_path = find_shortest_path(memory, start, target)
        if len(curr_path) == 0:
            return byte_pos
    return None


def main():
    byte_positions = parse_input()
    memory = create_memory_space(byte_positions, NUM_BYTES)
    start = BytePos(0, 0)
    target = BytePos(MAX_X, MAX_Y)
    path = find_shortest_path(memory, start, target)
    print("RESULT: ", len(path))
    result = solve_part_two(byte_positions)
    print("RESULT PART TWO: ", result)


if __name__ == "__main__":
    main()
