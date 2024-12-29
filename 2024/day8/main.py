from typing import NamedTuple
import itertools


class Pos(NamedTuple):
    row: int
    col: int

    def __sub__(self, other: "Pos"):
        return Pos(self.row - other.row, self.col - other.col)

    def __add__(self, other):
        return Pos(self.row + other.row, self.col + other.col)


def parse_grid(lines: list[str]):
    grid = []
    symbols: dict[str, list[Pos]] = {}
    for i, row in enumerate(lines):
        if row == "":
            continue
        grid.append([])
        for j, c in enumerate(row):
            grid[-1].append(c)
            if c == ".":
                continue
            if c not in symbols:
                symbols[c] = []
            symbols[c].append(Pos(i, j))

    return symbols, grid


def find_antinodes(
    symbols: dict[str, list[Pos]], grid: list[list[str]], extend_antinodes: bool = False
):
    def in_bounds(p: Pos) -> bool:
        return (
            p.row < len(grid) and p.row >= 0 and p.col < len(grid[p.row]) and p.col >= 0
        )

    antinodes: set[Pos] = set()
    for positions in symbols.values():
        for p1, p2 in itertools.combinations(positions, 2):
            vec1 = p1 - p2
            vec2 = p2 - p1
            if not extend_antinodes:
                a1 = p1 + vec1
                a2 = p2 + vec2
                if in_bounds(a1):
                    antinodes.add(a1)
                if in_bounds(a2):
                    antinodes.add(a2)
                continue
            while in_bounds(p1):
                antinodes.add(p1)
                p1 += vec1
            while in_bounds(p2):
                antinodes.add(p2)
                p2 += vec2
    return antinodes


def main():
    with open("input.txt") as file:
        lines = file.read().split("\n")
        symbols, grid = parse_grid(lines)
        antinodes = find_antinodes(symbols, grid, extend_antinodes=False)
        print("RESULT: ", len(antinodes))
        antinodes = find_antinodes(symbols, grid, extend_antinodes=True)
        print("RESULT PART TWO: ", len(antinodes))


if __name__ == "__main__":
    main()
