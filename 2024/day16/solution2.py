from collections import deque
from queue import PriorityQueue
from typing import DefaultDict
from shared import Pos, Maze, Direction, TURN_PENALTY, parse_maze, get_neighboors


def shortest_paths(start: Pos, start_dir: Direction, end: Pos, maze: Maze):
    q = PriorityQueue()
    end_states = set()
    q.put((0, start, start_dir))
    distances = {(start, start_dir): 0}
    distances = DefaultDict(lambda: float("inf"))
    distances[(start, start_dir)] = 0
    prev = DefaultDict(set)
    best_dist = float("inf")
    while not q.empty():
        dist, curr, dir = q.get()
        if dist > distances[(curr, dir)]:
            continue
        if curr == end:
            if dist > best_dist:
                break
            best_dist = dist
            end_states.add((curr, dir))
        neighboors = get_neighboors(curr, maze)
        for n, weight, turn_dir in neighboors:
            new_dist = dist + weight
            if turn_dir != dir:
                new_dist += TURN_PENALTY
            lowest = distances[(n, turn_dir)]
            if new_dist > lowest:
                continue
            if new_dist < lowest:
                prev[(n, turn_dir)] = set()
                distances[(n, turn_dir)] = new_dist
            prev[(n, turn_dir)].add((curr, dir))
            q.put((new_dist, n, turn_dir))
    states = deque(end_states)
    seen = set(end_states)
    while states:
        key = states.popleft()
        for last in prev.get(key, []):
            if last in seen:
                continue
            seen.add(last)
            states.append(last)
    return best_dist, len({p: d for p, d in seen})


def main():
    with open("input.txt") as file:
        maze_text = file.read().strip()
    start, end, maze = parse_maze(maze_text)
    answer1, answer2 = shortest_paths(start, "RIGHT", end, maze)
    print("RESULT: ", answer1)
    print("RESULT PART TWO: ", answer2)


if __name__ == "__main__":
    main()
