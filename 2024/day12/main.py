from typing import NamedTuple

type FarmGrid = list[list[str]]
type FarmArea = tuple[list[GridPos], set[GridPos]]
type Perimiters = list[FarmArea]


class GridPos(NamedTuple):
    row: int
    col: int


def parse_input(input: str) -> FarmGrid:
    grid: FarmGrid = []
    for line in input.split("\n"):
        if line:
            grid.append([c for c in line])
    return grid


def check_bounds(rows: int, cols: int, pos: GridPos):
    return pos.row < rows and pos.row >= 0 and pos.col < cols and pos.col >= 0


def define_perimiters(grid: FarmGrid):

    visited: set[GridPos] = set()
    perimiters: Perimiters = []
    rows, cols = len(grid), len(grid[0])

    def dfs(pos: GridPos) -> FarmArea:
        visited.add(pos)
        area, fences = {pos}, []

        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for row_offset, col_offset in offsets:
            p = GridPos(pos.row + row_offset, pos.col + col_offset)
            if not check_bounds(rows, cols, p) or grid[p.row][p.col] != crop:
                fences.append(p)
                continue
            if p in visited:
                continue
            d_fences, d_area = dfs(p)
            for a in d_area:
                area.add(a)
            fences += d_fences
        return fences, area

    for i in range(rows):
        for j in range(cols):
            pos = GridPos(i, j)
            if pos in visited:
                continue
            crop = grid[pos.row][pos.col]
            perim = dfs(pos)
            perimiters.append(perim)
    return perimiters


def get_num_corners(area: set[GridPos]) -> int:
    def is_corner(
        row_neighbor: GridPos,
        col_neighbor: GridPos,
        diagonal_neighbor: GridPos,
    ):
        row_neighbor_in_area = row_neighbor in area
        col_neighbor_in_area = col_neighbor in area
        return (not row_neighbor_in_area and not col_neighbor_in_area) or (
            row_neighbor_in_area
            and col_neighbor_in_area
            and diagonal_neighbor not in area
        )

    num_corners = 0
    for pos in area:
        offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for row_offset, col_offset in offsets:
            row_neighbor = GridPos(pos.row + row_offset, pos.col)
            col_neighbor = GridPos(pos.row, pos.col + col_offset)
            diagonal_neighbor = GridPos(pos.row + row_offset, pos.col + col_offset)
            num_corners += is_corner(row_neighbor, col_neighbor, diagonal_neighbor)
    return num_corners


def calculate_costs(perimiters: Perimiters) -> tuple[int, int]:
    costs = 0
    side_costs = 0
    for fences, area in perimiters:
        area_size = len(area)
        costs += len(fences) * area_size
        side_costs += get_num_corners(area) * area_size
    return costs, side_costs


def main():
    with open("input.txt") as file:
        input = file.read()
        grid = parse_input(input)
        perimiters = define_perimiters(grid)
        costs = calculate_costs(perimiters)
        print("RESULTS: ", costs)


if __name__ == "__main__":
    main()
