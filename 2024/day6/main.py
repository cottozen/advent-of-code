import enum
from typing import NamedTuple


class GridSquare(enum.StrEnum):
    Start = "S"
    Object = "#"
    PlacedObject = "0"
    Path = "."
    GuardUp = "^"
    GuardDown = "v"
    GuardRight = ">"
    GuardLeft = "<"
    GuardVisitedVertical = "|"
    GuardVisitedHorizontal = "-"
    GuardVisitedBothDirections = "+"

    @classmethod
    def from_str(cls, x: str) -> "GridSquare":
        for v in GridSquare:
            if v.value == x:
                return v
        raise ValueError(f"Invalid GridItem value: {x}")

    @staticmethod
    def is_guard(x: "GridSquare") -> bool:
        return x in (
            GridSquare.GuardUp,
            GridSquare.GuardDown,
            GridSquare.GuardLeft,
            GridSquare.GuardRight,
        )


type GridArea = list[list[GridSquare]]


class GridPos(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        assert isinstance(other, GridPos), "Cant add different types."
        return GridPos(self.row + other.row, self.col + other.col)


GUARD_TURN_DIRECTION = {
    GridSquare.GuardUp: GridSquare.GuardRight,
    GridSquare.GuardDown: GridSquare.GuardLeft,
    GridSquare.GuardRight: GridSquare.GuardDown,
    GridSquare.GuardLeft: GridSquare.GuardUp,
}
GUARD_VISITED = {
    GridSquare.GuardUp: GridSquare.GuardVisitedVertical,
    GridSquare.GuardDown: GridSquare.GuardVisitedVertical,
    GridSquare.GuardRight: GridSquare.GuardVisitedHorizontal,
    GridSquare.GuardLeft: GridSquare.GuardVisitedHorizontal,
}

GUARD_STEP_CHANGE = {
    GridSquare.GuardUp: GridPos(-1, 0),
    GridSquare.GuardDown: GridPos(1, 0),
    GridSquare.GuardRight: GridPos(0, 1),
    GridSquare.GuardLeft: GridPos(0, -1),
}


class Map:

    def __init__(self, guard_pos: GridPos, grid: GridArea):
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.guard_pos = guard_pos
        self._guard = self[self.guard_pos]
        self._guard_start_pos = self.guard_pos
        self._guard_start = self._guard
        self[self.guard_pos] = GridSquare.Start
        self.visited: list[tuple[GridPos, GridSquare]] = []

    def num_visited(self) -> int:
        return len({p for p, _ in self.visited})

    def reset_guard(self):
        self.guard = self._guard_start
        self.guard_pos = self._guard_start_pos
        self[self.guard_pos] = self.guard

    @classmethod
    def create(cls, input: str) -> "Map":
        grid = []
        rows = input.split("\n")
        guard_pos: GridPos = GridPos(0, 0)
        for i, row in enumerate(rows):
            if row.strip() == "":
                break
            grid.append([])
            for j, col in enumerate(row):
                square = GridSquare.from_str(col)
                if GridSquare.is_guard(square):
                    guard_pos = GridPos(i, j)
                grid[-1].append(square)
        return cls(guard_pos, grid)

    @property
    def guard(self) -> GridSquare:
        return self._guard

    @guard.setter
    def guard(self, value: GridSquare) -> None:
        assert GridSquare.is_guard(value), "invalid guard value"
        self._guard = value

    @property
    def guard_step(self) -> GridPos:
        return GUARD_STEP_CHANGE[self.guard]

    def in_bound(self, pos: GridPos) -> bool:
        return (
            pos.row < self.rows
            and pos.row >= 0
            and pos.col < self.cols
            and pos.col >= 0
        )

    def __getitem__(self, pos: GridPos) -> GridSquare:
        return self.grid[pos.row][pos.col]

    def __setitem__(self, pos: GridPos, item: GridSquare) -> None:
        self.grid[pos.row][pos.col] = item

    def _get_visit_value(self):
        return GUARD_VISITED[self.guard]

    def visit(self) -> bool:
        current_value = self[self.guard_pos]
        new_value = self._get_visit_value()
        if (
            current_value == GridSquare.GuardVisitedVertical
            and new_value == GridSquare.GuardVisitedHorizontal
        ) or (
            current_value == GridSquare.GuardVisitedHorizontal
            and new_value == GridSquare.GuardVisitedVertical
        ):
            new_value = GridSquare.GuardVisitedBothDirections
        elif (
            self.guard_pos,
            self.guard,
        ) in self.visited:
            return True
        self[self.guard_pos] = new_value
        if len(self.visited) == 0 or self.visited[-1][0] != self.guard_pos:
            self.visited.append((self.guard_pos, self.guard))
        return False

    def step(self) -> bool:
        loop = self.visit()
        if loop:
            return loop
        new_pos = self.guard_pos + self.guard_step
        if not self.in_bound(new_pos):
            self.guard_pos = new_pos
        elif (
            self[new_pos] != GridSquare.Object
            and self[new_pos] != GridSquare.PlacedObject
        ):
            self.guard_pos = new_pos
        else:
            self.guard = GUARD_TURN_DIRECTION[self.guard]
        return False

    def walk(self, debug: bool = False) -> bool:
        self.visited = []
        while self.in_bound(self.guard_pos):
            loop = self.step()
            if loop:
                return True
            if debug:
                self.display()
        return False

    def solve_part_two(self, debug: bool = False) -> list[GridPos]:
        loops = []
        positions_to_explore = [(pos, v) for pos, v in self.visited]
        attempted_positions = set()

        def reset():
            for pos, _ in self.visited:
                self[pos] = GridSquare.Path
            self.visited = []

        for i in range(0, len(positions_to_explore) - 1):
            object_pos, _ = positions_to_explore[i + 1]
            if object_pos in attempted_positions:
                continue
            # prevent doing the same work twice
            attempted_positions.add(object_pos)
            # Reset map
            reset()
            # Move guard to right before placed object to reduce steps.
            self.guard_pos, self.guard = positions_to_explore[i]
            # place object
            self[object_pos] = GridSquare.PlacedObject
            if self.walk(debug=debug):
                loops.append(object_pos)
            self[object_pos] = GridSquare.Path
        return loops

    def _format_grid(self, grid: GridArea):
        text_grid = "\n"
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                v = col
                if i == self.guard_pos.row and j == self.guard_pos.col:
                    v = self.guard
                elif i == self._guard_start_pos.row and j == self._guard_start_pos.col:
                    v = GridSquare.Start
                text_grid += v.value
            text_grid += "\n"
        return text_grid

    def display(self):
        print("===============================")
        # draw guard
        text_grid = self._format_grid(self.grid)
        print(text_grid)


def main():
    with open("input.txt", "r") as file:
        map = Map.create(file.read())
    map.walk(debug=False)
    result = map.num_visited()
    print("Result: ", result)
    loops = map.solve_part_two()
    print("Result part two: ", len(loops))


if __name__ == "__main__":
    main()
