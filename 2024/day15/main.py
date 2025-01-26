from typing import Literal, NamedTuple, cast


type Square = Literal["#", ".", "O", "@"]
type Step = Literal["<", "v", ">", "^"]


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x = self.x + other[0]
        y = self.y + other[1]
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other[0]
        y = self.y - other[1]
        return Vector(x, y)


Vectors: dict[Step, Vector] = {
    "<": Vector(-1, 0),
    "v": Vector(0, 1),
    ">": Vector(1, 0),
    "^": Vector(0, -1),
}


type WarehouseGrid = list[list[Square]]


class Warehouse:
    def __init__(self, robot: Vector, grid: WarehouseGrid):
        self.robot = robot
        self.grid = grid

        self.resized = False

    def resize(self):
        self.resized = True
        grid = []
        mapping = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@.",
        }
        for i, row in enumerate(self.grid):
            cols = []
            for j, col in enumerate(row):
                cols += [n for n in mapping[col]]
            grid.append(cols)
        self._update_robot(Vector(self.robot.x, 0))
        self.grid = grid

    def get_gps_coordinates(self):
        total = 0
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                pos = Vector(j, i)
                if self[pos] == "O" or self[pos] == "[":
                    total += pos.y * 100 + pos.x
        return total

    def _update_robot(self, vec: Vector):
        self[self.robot] = "."
        self.robot += vec
        self[self.robot] = "@"

    def _box_dfs(
        self,
        pos: Vector,
        vec: Vector,
        boxes: set[Vector],
    ) -> set[Vector] | None:
        """
        Finds all boxes in given direction
        """
        if self[pos] == "#":
            return None
        elif self[pos] == ".":
            return set()
        boxes.add(pos)
        for box in (
            pos + (Vectors[">"] if self[pos] == "[" else Vectors["<"]),
            pos + vec,
        ):
            if box in boxes:
                continue
            b = self._box_dfs(box, vec, boxes)
            if b is None:
                return None
            boxes = boxes.union(b)
        return boxes

    def _apply_box_updates(self, vec: Vector, boxes: set[Vector]):
        update_map = {}
        for box in boxes:
            new_pos = box + vec
            if box not in update_map:
                update_map[box] = "."
            if new_pos not in update_map or (
                (curr := update_map[new_pos]) and curr == "."
            ):
                update_map[new_pos] = self[box]
        for box, box_square in update_map.items():
            self[box] = box_square

    def _move_robot_resized(self, vec: Vector):
        boxes = self._box_dfs(self.robot + vec, vec, set())
        if boxes is None:
            return
        self._apply_box_updates(vec, boxes)
        self._update_robot(vec)

    def _move_robot(self, vec: Vector):
        if self.resized:
            return self._move_robot_resized(vec)
        boxes = []
        new_pos = self.robot + vec
        while self[new_pos] == "O":
            boxes.append(new_pos)
            if self[new_pos + vec] == "#":
                break
            new_pos = new_pos + vec
        # move boxes, Check if they can be moved
        if self[new_pos] == ".":
            while len(boxes):
                box = boxes.pop()
                self[box + vec] = "O"
        if len(boxes) == 0:
            self._update_robot(vec)

    def move_robot(self, vec: Vector):
        if self.resized:
            return self._move_robot_resized(vec)
        return self._move_robot(vec)

    def __getitem__(self, pos: Vector) -> Square:
        return self.grid[pos.y][pos.x]

    def __setitem__(self, pos: Vector, square: Square):
        self.grid[pos.y][pos.x] = square

    def display(self):
        for row in self.grid:
            print("".join(row))


def parse_input(input: str) -> tuple[Warehouse, list[Step]]:
    [warehouse, steps] = input.split("\n\n")

    warehouse_grid: WarehouseGrid = []
    rows = warehouse.split("\n")
    robot = (0, 0)
    for i, row in enumerate(rows):
        cols = []
        for j, c in enumerate(row):
            if c == "@":
                robot = (j, i)
            cols.append(cast(Square, c))
        warehouse_grid.append(cols)
    return Warehouse(robot=Vector(*robot), grid=warehouse_grid), [
        cast(Step, s) for s in steps if s != "\n"
    ]


def simulate_steps(warehouse: Warehouse, steps: list[Step]):
    for step in steps:
        vec = Vectors[step]
        if warehouse[warehouse.robot + vec] == "#":
            continue
        warehouse.move_robot(vec)
    return warehouse


def main():
    with open("input.txt") as file:
        input = file.read().strip()
        warehouse, steps = parse_input(input)
        simulate_steps(warehouse, steps)
        result = warehouse.get_gps_coordinates()
        print("RESULT: ", result)
        warehouse, steps = parse_input(input)
        warehouse.resize()
        simulate_steps(warehouse, steps)
        result = warehouse.get_gps_coordinates()
        print("RESULT PART TWO: ", result)


if __name__ == "__main__":
    main()
