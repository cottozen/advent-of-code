def parse_trail_map(lines: list[str]):
    grid = []
    for row in lines:
        if row == "":
            continue
        grid.append([int(c) for c in row])
    return grid


def find_paths(trail_map: list[list[int]]):
    def dfs(
        i: int,
        j: int,
        path: list[tuple[int, int]],
        solutions: (
            list[list[tuple[int, int]]] | dict[tuple[int, int], list[tuple[int, int]]]
        ),
    ):
        path.append((i, j))
        v = trail_map[i][j]
        if v == 9:
            if isinstance(solutions, dict):
                solutions[(i, j)] = path
            else:
                solutions.append(path)
            return solutions

        def is_next(i: int, j: int):
            return trail_map[i][j] - v == 1

        if i + 1 < len(trail_map) and is_next(i + 1, j):
            dfs(i + 1, j, [p for p in path], solutions)
        if i - 1 >= 0 and is_next(i - 1, j):
            dfs(i - 1, j, [p for p in path], solutions)
        if j + 1 < len(trail_map[i]) and is_next(i, j + 1):
            dfs(i, j + 1, [p for p in path], solutions)
        if j - 1 >= 0 and is_next(i, j - 1):
            dfs(i, j - 1, [p for p in path], solutions)
        return solutions

    result = 0
    result_part_two = 0
    for i in range(len(trail_map)):
        for j in range(len(trail_map[i])):
            v = trail_map[i][j]
            if v == 0:
                solutions = dfs(i, j, [], {})
                result += len(solutions)
                solutions = dfs(i, j, [], [])
                result_part_two += len(solutions)
    return result, result_part_two


def main():
    with open("input.txt") as file:
        lines = file.read().splitlines()
        trail = parse_trail_map(lines)
        result, result_part_two = find_paths(trail)
        print("RESULT: ", result)
        print("RESULT PART TWO: ", result_part_two)


if __name__ == "__main__":
    main()
