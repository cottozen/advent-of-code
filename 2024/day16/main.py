from typing import DefaultDict, Literal
from queue import PriorityQueue

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


def track_path(prev, end) -> list[list[Pos]]:
    paths = []

    def backtrack(path, node):
        if node not in prev:
            # reverse path to right order: start => end
            paths.append(path[::-1])
            return
        for p in prev[node]:
            if p in path:
                continue
            backtrack(path + [p], p)

    backtrack([end], end)
    return paths


def dijkstra(maze: Maze, start: Pos, start_dir: Direction):
    q: PriorityQueue = PriorityQueue()
    q.put((0, start, start_dir))
    distances: dict[Pos, float] = {start: 0}
    visited = set()
    prev: dict[Pos, Pos] = {}

    while not q.empty():
        _, curr, curr_dir = q.get()
        if curr in visited:
            continue
        visited.add(curr)
        neighboors = get_neighboors(curr, maze)
        for n, w, d in neighboors:
            new_dist = distances[curr] + w
            if d != curr_dir:
                new_dist += TURN_PENALTY
            if n not in distances or new_dist < distances[n]:
                distances[n] = new_dist
                prev[n] = curr
                q.put((new_dist, n, d))
    return prev, distances


def find_shortest_path(start: Pos, start_dir: Direction, end: Pos, maze: Maze):
    prev, distances = dijkstra(maze, start, start_dir)
    curr = end
    reverse_distances = {}
    turns = set()
    while curr:
        reverse_dist = distances[end] - distances[curr]
        reverse_distances[curr] = reverse_dist
        new_curr = prev.get(curr)
        if new_curr:
            if abs(distances[curr] - distances[new_curr]) == 1001:
                turns.add(new_curr)
        curr = new_curr
    return reverse_distances, turns


def setup_state(start: Pos, start_dir: Direction):
    q: PriorityQueue = PriorityQueue()
    q.put((0, start, start_dir))
    distances: dict[Pos, float] = {start: 0}
    visited = set()
    prev: dict[Pos, list[Pos]] = DefaultDict(list)
    return q, distances, visited, prev


def shortest_paths(start: Pos, start_dir: Direction, end: Pos, maze: Maze):
    reverse_distances, turns = find_shortest_path(start, start_dir, end, maze)
    q, distances, visited, prev = setup_state(start, start_dir)
    while not q.empty():
        _, curr, curr_dir = q.get()
        if curr in visited:
            continue
        visited.add(curr)
        neighboors = get_neighboors(curr, maze)
        for n, w, d in neighboors:
            new_dist = distances[curr] + w
            if d != curr_dir:
                new_dist += TURN_PENALTY
            if n not in distances or new_dist <= distances[n]:
                distances[n] = new_dist
                prev[n].append(curr)
                q.put((new_dist, n, d))
                pass
            if (
                n in turns
                # if we can get to the turn point with turning and the total remaining distance is the same then we explore
                and (reverse_distances[n] + new_dist - TURN_PENALTY)
                == reverse_distances[start]
            ):
                prev[n].append(curr)
                new_turns = set()
                while curr not in reverse_distances:
                    reverse_distances[curr] = reverse_distances[start] - distances[curr]
                    new_curr = prev[curr][-1]
                    if abs(distances[curr] - distances[new_curr]) == TURN_PENALTY + 1:
                        new_turns.add(new_curr)
                    curr = new_curr
                if len(new_turns):
                    turns = turns.union(new_turns)
                    q, distances, visited, prev = setup_state(start, start_dir)
                    break
    paths = track_path(prev, end)
    return paths, distances


def display_maze(maze: Maze):
    print("\n".join("".join(row) for row in maze))


def display_paths(maze: Maze, paths: list[list[Pos]], track: MazeSquare = "@"):
    for path in paths:
        for i, (r, c) in enumerate(path):
            if i == 0:
                maze[r][c] = "S"
            elif i == len(path) - 1:
                maze[r][c] = "E"
            else:
                maze[r][c] = track
        display_maze(maze)
        for r, c in path:
            maze[r][c] = "."


def count_best_tiles(paths: list[list[Pos]]) -> int:
    best_path_tiles = set()
    for path in paths:
        for pos in path:
            best_path_tiles.add(pos)
    return len(best_path_tiles)


def main():
    with open("input.txt") as file:
        maze_text = file.read().strip()
    start, end, maze = parse_maze(maze_text)
    paths, distances = shortest_paths(start, "RIGHT", end, maze)
    print("RESULT: ", distances.get(end))
    print("RESULT PART TWO: ", count_best_tiles(paths))


if __name__ == "__main__":
    main()
