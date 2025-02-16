from queue import PriorityQueue
from typing import DefaultDict, NamedTuple


# FILE_PATH = "example.txt"
FILE_PATH = "input.txt"

type Grid = list[list[str]]


class GridPos(NamedTuple):
    row: int
    col: int


def parse_input() -> Grid:
    grid = []
    with open(FILE_PATH, "r") as file:
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


def get_neighbours(p: GridPos, grid: Grid):
    neighbours = []
    cheat_neighbours = []

    if p.row > 0:
        neighbours.append(GridPos(p.row - 1, p.col))
    if p.row < len(grid) - 1:
        neighbours.append(GridPos(p.row + 1, p.col))
    if p.col > 0:
        neighbours.append(GridPos(p.row, p.col - 1))
    if p.col < len(grid[0]) - 1:
        neighbours.append(GridPos(p.row, p.col + 1))

    if p.row > 1 and grid[p.row - 1][p.col] == "#":
        cheat_neighbours.append(GridPos(p.row - 2, p.col))
    if p.row < (len(grid) - 2) and grid[p.row + 1][p.col] == "#":
        cheat_neighbours.append(GridPos(p.row + 2, p.col))
    if p.col > 1 and grid[p.row][p.col - 1] == "#":
        cheat_neighbours.append(GridPos(p.row, p.col - 2))
    if p.col < (len(grid[0]) - 2) and grid[p.row][p.col + 1] == "#":
        cheat_neighbours.append(GridPos(p.row, p.col + 2))

    neighbours = [n for n in neighbours if grid[n.row][n.col] != "#"]
    return neighbours, [(p, n) for n in cheat_neighbours if grid[n.row][n.col] != "#"]


def dijkstra(start: GridPos, end: GridPos, grid: Grid):
    q = PriorityQueue()
    q.put((0, start))
    prev: dict[GridPos, GridPos] = dict()
    visited: set[GridPos] = set()
    distances = DefaultDict(lambda: float("inf"))
    distances[start] = 0
    neighbours_cheats = []

    while not q.empty():
        dist, curr = q.get()
        if curr in visited:
            continue
        visited.add(curr)

        neighbours, cheats = get_neighbours(curr, grid)
        neighbours_cheats += cheats
        for n in neighbours:
            new_dist = dist + 1
            q.put((new_dist, n))

            if distances[n] > new_dist:
                distances[n] = new_dist
                prev[n] = curr
    curr = end
    return distances, set(neighbours_cheats)


def find_cheat_paths(grid: Grid, min_benefit: int):

    start, end = find_start_and_end(grid)

    travel_distances, cheat_neighbours = dijkstra(start, end, grid)
    distances_left, _ = dijkstra(end, start, grid)
    worse_path_len = travel_distances[end]
    cheat_paths = []
    for cheat_start, cheat_end in cheat_neighbours:
        new_dist = travel_distances[cheat_start] + distances_left[cheat_end] + 2
        if (worse_path_len - new_dist) >= min_benefit:
            cheat_paths.append((cheat_start, cheat_end))

    return cheat_paths


def main():
    grid = parse_input()
    display_grid(grid)
    cheat_paths = find_cheat_paths(grid, 100)
    print("RESULT: ", len(cheat_paths))


if __name__ == "__main__":
    main()
