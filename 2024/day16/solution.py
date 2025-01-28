from typing import DefaultDict
from queue import PriorityQueue
from shared import Pos, Maze, Direction, TURN_PENALTY, parse_maze, get_neighboors


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


def find_shortest_path(start: Pos, start_dir: Direction, end: Pos, maze: Maze):
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


def shortest_paths(start: Pos, start_dir: Direction, end: Pos, maze: Maze):
    def setup_state():
        q: PriorityQueue = PriorityQueue()
        q.put((0, start, start_dir))
        distances: dict[Pos, float] = {start: 0}
        visited = set()
        prev: dict[Pos, list[Pos]] = DefaultDict(list)
        return q, distances, visited, prev

    reverse_distances, turns = find_shortest_path(start, start_dir, end, maze)
    q, distances, visited, prev = setup_state()
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
                    q, distances, visited, prev = setup_state()
                    break
    paths = track_path(prev, end)
    return paths, distances


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
