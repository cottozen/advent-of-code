import numpy as np
from typing import NamedTuple


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
    return grid


def display_grid(grid: Grid):
    for row in grid:
        print("".join(row))


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


def find_cheats(
    cheat_start: GridPos,
    path: dict[GridPos, int],
    grid: Grid,
    max_distance: int,
    target: int,
):
    num_cheats = 0

    pre_walked_steps = path[cheat_start]

    max_row = min(cheat_start.row + max_distance, len(grid) + 1)
    max_col = min(cheat_start.col + max_distance, len(grid[0]) + 1)
    min_row = max(cheat_start.row - max_distance, 0)
    min_col = max(cheat_start.col - max_distance, 0)
    for i in range(min_row, max_row + 1):
        row_offset = min(abs(cheat_start.row - i), 0)
        for j in range(min_col + row_offset, max_col + 1 - row_offset):
            cheat_end = GridPos(i, j)
            if cheat_end not in path:
                continue
            dy, dx = abs(cheat_end.row - cheat_start.row), abs(
                cheat_end.col - cheat_start.col
            )
            dist = dy + dx
            cheat_value = path[cheat_end] - dist - pre_walked_steps
            if dist <= max_distance and cheat_value >= target:
                num_cheats += 1
    return num_cheats


def dfs(grid: Grid):
    start, _ = find_start_and_end(grid)
    path = []
    stack = [start]
    visited = set()
    while len(stack):
        curr = stack.pop()
        path.append(curr)
        visited.add(curr)
        neighbours = get_neighbours(curr, grid)
        for n in neighbours:
            if n in visited or grid[n.row][n.col] != ".":
                continue
            stack.append(n)
    return path


def solve(grid: Grid, cheat_dist: int, min_benefit: int):
    path = dfs(grid)
    path_dist = {p: i for i, p in enumerate(path)}
    return np.sum(
        [
            find_cheats(cheat_start, path_dist, grid, cheat_dist, min_benefit)
            for cheat_start in path
        ]
    )


def main():
    grid = parse_input("input.txt")
    num_cheats = solve(grid, 2, 100)
    print("RESULT: ", num_cheats)
    num_cheats = solve(grid, 20, 100)
    print("RESULT PART TWO: ", num_cheats)


if __name__ == "__main__":
    main()
