from typing import Literal

type MazeSquare = Literal["#", ".", "E", "S", "@"]

type Maze = list[list[MazeSquare]]

type Pos = tuple[int, int]


type Direction = Literal["UP", "RIGHT", "DOWN", "LEFT"]

VECTOR_MAPPING: dict[tuple[int, int], Direction] = {
    (1, 0): "DOWN",
    (-1, 0): "UP",
    (0, 1): "RIGHT",
    (0, -1): "LEFT",
}

TURN_PENALTY = 1000

START_DIR: Direction = "RIGHT"


def parse_maze(maze: str) -> tuple[Pos, Pos, Maze]:
    grid: Maze = []
    start: Pos = (0, 0)
    end: Pos = (0, 0)
    for i, row in enumerate(maze.split("\n")):
        cols = []
        for j, col in enumerate(row):
            if col == "S":
                start = (i, j)
            if col == "E":
                end = (i, j)
            cols.append(col)
        grid.append(cols)
    return start, end, grid


def get_neighboors(p: Pos, maze: Maze) -> list[tuple[Pos, int, Direction]]:
    rows, cols = len(maze), len(maze[0])
    neighboors = []
    r, c = p
    weight = 1
    if r + 1 < rows:
        neighboors.append(((r + 1, c), weight, "UP"))
    if r - 1 >= 0:
        neighboors.append(((r - 1, c), weight, "DOWN"))
    if c + 1 < cols:
        neighboors.append(((r, c + 1), weight, "RIGHT"))
    if c - 1 >= 0:
        neighboors.append(((r, c - 1), weight, "LEFT"))
    return [((r, c), w, d) for (r, c), w, d in neighboors if maze[r][c] != "#"]
