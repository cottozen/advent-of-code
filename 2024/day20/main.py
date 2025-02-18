from collections import deque
from queue import PriorityQueue
from typing import DefaultDict, NamedTuple
import copy


type Grid = list[list[str]]


class GridPos(NamedTuple):
    row: int
    col: int


def parse_input(file_path: str) -> Grid:
    grid = []
    with open(file_path, "r") as file:
        rows = file.readlines()
        for row in rows:
            grid.append([c for c in row.strip()])
    # remove out layer of walls
    return grid


def display_grid(grid: Grid):
    for row in grid:
        print("".join(row))


def display_cheat_path(cheat_path: list[GridPos], grid: Grid):
    start, end = find_start_and_end(grid)
    grid_copy = copy.deepcopy(grid)
    for i, p in enumerate(cheat_path):
        grid_copy[p.row][p.col] = str(i)
    grid_copy[start.row][start.col] = "S"
    grid_copy[end.row][end.col] = "E"
    display_grid(grid_copy)


def find_start_and_end(grid: Grid) -> tuple[GridPos, GridPos]:
    start, end = GridPos(0, 0), GridPos(0, 0)
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                start = GridPos(i, j)
            if col == "E":
                end = GridPos(i, j)
    return start, end


def get_neighbours(p: GridPos, grid: Grid) -> list[GridPos]:
    neighbours = []
    NUM_ROWS = len(grid) - 2
    NUM_COLS = len(grid[0]) - 2
    if p.row > 1:
        neighbours.append(GridPos(p.row - 1, p.col))
    if p.row < NUM_ROWS:
        neighbours.append(GridPos(p.row + 1, p.col))
    if p.col > 1:
        neighbours.append(GridPos(p.row, p.col - 1))
    if p.col < NUM_COLS:
        neighbours.append(GridPos(p.row, p.col + 1))
    return neighbours


def dijkstra(start: GridPos, grid: Grid):
    q = PriorityQueue()
    q.put((0, start))
    prev: dict[GridPos, GridPos] = dict()
    visited: set[GridPos] = set()
    distances = DefaultDict(lambda: float("inf"))
    distances[start] = 0

    while not q.empty():
        dist, curr = q.get()
        if curr in visited:
            continue
        visited.add(curr)

        neighbours = get_neighbours(curr, grid)
        for n in neighbours:
            if grid[n.row][n.col] == "#":
                continue
            new_dist = dist + 1
            q.put((new_dist, n))

            if distances[n] > new_dist:
                distances[n] = new_dist
                prev[n] = curr
    return prev, distances


def construct_path(end: GridPos, prev: dict[GridPos, GridPos]) -> list[GridPos]:
    curr = end
    path = []
    while curr:
        path.append(curr)
        curr = prev.get(curr)
    return list(reversed(path))


def find_cheat_end_positions(
    cheat_start: GridPos,
    grid: Grid,
    max_distance: int,
):
    q = deque([(cheat_start, 0)])
    visited: set = {cheat_start}
    cheat_end_positions: list[tuple[GridPos, int]] = []
    prev: dict[GridPos, GridPos] = {}
    while q:
        curr, dist = q.popleft()
        if dist > max_distance:
            continue
        neighbours = get_neighbours(curr, grid)
        for n in neighbours:
            entry = (n, dist + 1)
            if n == cheat_start:
                continue
            if n in visited:
                continue
            prev[n] = curr
            visited.add(n)
            q.append(entry)
        if curr != cheat_start and grid[curr.row][curr.col] != "#":
            cheat_end_positions.append((curr, dist))

    return cheat_end_positions


def find_cheat_paths(
    grid: Grid, cheat_dist: int, min_benefit: int, use_exact_match: bool = False
):

    start, end = find_start_and_end(grid)
    prev, travel_distances = dijkstra(start, grid)
    path = construct_path(end, prev)
    worse_path_len = travel_distances[end]

    cheat_paths = set()
    for cheat_start in path:
        cheat_end_positions = find_cheat_end_positions(cheat_start, grid, cheat_dist)
        for cheat_end, cheat_dist in cheat_end_positions:
            left = worse_path_len - travel_distances[cheat_end]
            traveled = travel_distances[cheat_start]
            new_dist = traveled + left + cheat_dist
            is_valid = (
                (worse_path_len - new_dist) == min_benefit
                if use_exact_match
                else (worse_path_len - new_dist) >= min_benefit
            )
            if is_valid:
                cheat_paths.add((cheat_start, cheat_end))
    return cheat_paths


TESTS_PART_ONE = [
    (14, 2, 2),
    (14, 4, 2),
    (2, 6, 2),
    (4, 8, 2),
    (2, 10, 2),
    (3, 12, 2),
    (1, 20, 2),
    (1, 36, 2),
    (1, 38, 2),
    (1, 40, 2),
    (1, 64, 2),
]

TESTS_PART_TWO = [
    (32, 50, 20),
    (31, 52, 20),
    (29, 54, 20),
    (39, 56, 20),
    (25, 58, 20),
    (23, 60, 20),
    (20, 62, 20),
    (19, 64, 20),
    (12, 66, 20),
    (14, 68, 20),
    (12, 70, 20),
    (22, 72, 20),
    (4, 74, 20),
    (3, 76, 20),
]


def test():
    grid = parse_input("example.txt")
    print("TEST PART ONE")
    for expected, picoseconds, num_cheat_steps in TESTS_PART_ONE:
        cheat_paths = find_cheat_paths(
            grid, num_cheat_steps, picoseconds, use_exact_match=True
        )
        try:
            assert (
                len(cheat_paths) == expected
            ), f"failed on {expected} != {len(cheat_paths)}, {expected, picoseconds, num_cheat_steps}"
        except Exception as ex:
            print(ex)
    print("TEST PART TWO")
    for expected, picoseconds, num_cheat_steps in TESTS_PART_TWO:
        cheat_paths = find_cheat_paths(
            grid, num_cheat_steps, picoseconds, use_exact_match=True
        )
        try:
            assert (
                len(cheat_paths) == expected
            ), f"failed on {expected} != {len(cheat_paths)}, {expected, picoseconds, num_cheat_steps}"
        except Exception as ex:
            print(ex)


def main():
    grid = parse_input("input.txt")
    cheat_paths = find_cheat_paths(grid, 2, 100)
    print("RESULT: ", len(cheat_paths))
    cheat_paths = find_cheat_paths(grid, 20, 100)
    print("RESULT PART TWO: ", len(cheat_paths))


if __name__ == "__main__":
    test()
    main()
