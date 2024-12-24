type LetterGrid = list[list[str]]

XMAS = ["X", "M", "A", "S"]
REVERSE_XMAS = ["S", "A", "M", "X"]

MAS = XMAS[1:]
MAS_REVERSE = REVERSE_XMAS[:-1]


def get_diagonal_letters(
    grid: LetterGrid,
    i: int,
    j: int,
    row_increment: int,
    col_increment: int,
    letter_count: int,
):
    letters = []
    for _ in range(letter_count + 1):
        letters.append(grid[i][j])
        i += row_increment
        j += col_increment
    return letters


def check_xmas_directions(grid: LetterGrid, i: int, j: int) -> int:
    def is_xmas(t: list[str]) -> bool:
        return t == XMAS or t == REVERSE_XMAS

    def get_xmas_diagnonal_letters(row_increment: int, col_increment: int):
        return get_diagonal_letters(grid, i, j, row_increment, col_increment, 3)

    directions: int = 0

    top_bound = i - 3 >= 0
    bottom_bound = i + 3 < len(grid)
    right_bound = j + 3 < len(grid[i])
    left_bound = j - 3 >= 0
    # left
    if left_bound:
        directions += is_xmas(grid[i][j - 3 : j + 1])
    # right
    if right_bound:
        directions += is_xmas(grid[i][j : j + 4])
    # top
    if top_bound:
        directions += is_xmas([row[j] for row in grid[i - 3 : i + 1]])
    # bottom
    if bottom_bound:
        directions += is_xmas([row[j] for row in grid[i : i + 4]])
    # top left
    if left_bound and top_bound:
        letters = get_xmas_diagnonal_letters(-1, -1)
        directions += is_xmas(letters)
    # top right
    if right_bound and top_bound:
        letters = get_xmas_diagnonal_letters(-1, 1)
        directions += is_xmas(letters)
    # bottom left
    if left_bound and bottom_bound:
        letters = get_xmas_diagnonal_letters(1, -1)
        directions += is_xmas(letters)
    # bottom right
    if right_bound and bottom_bound:
        letters = get_xmas_diagnonal_letters(1, 1)
        directions += is_xmas(letters)
    return directions


def check_xmas_directions_part_two(grid: LetterGrid, i: int, j: int) -> int:
    def is_word(t: list[str]) -> bool:
        return t == MAS or t == MAS_REVERSE

    def get_mas_diagnonal_letters(
        i: int, j: int, row_increment: int, col_increment: int
    ):
        return get_diagonal_letters(grid, i, j, row_increment, col_increment, 2)

    top_bound = i - 1 >= 0
    bottom_bound = i + 1 < len(grid)
    right_bound = j + 1 < len(grid[0])
    left_bound = j - 1 >= 0
    if top_bound and left_bound and bottom_bound and right_bound:
        if is_word(get_mas_diagnonal_letters(i - 1, j + 1, 1, -1)) and is_word(
            get_mas_diagnonal_letters(i - 1, j - 1, 1, 1)
        ):
            return 1
    return 0


def find_xmas(grid: LetterGrid) -> int:
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            letter = grid[i][j]
            if letter == "X":
                result += check_xmas_directions(grid, i, j)
    return result


def find_xmas_part_two(grid: LetterGrid) -> int:
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            letter = grid[i][j]
            if letter == "A":
                result += check_xmas_directions_part_two(grid, i, j)
    return result


if __name__ == "__main__":
    grid = []
    with open("input.txt", "r") as file:
        rows = file.readlines()
        for row in rows:
            grid.append([c for c in row])

    print(f"ROWS: {len(grid)}, COLS={len(grid[0])}")
    res = find_xmas(grid)
    print("Result: ", res)

    res = find_xmas_part_two(grid)
    print("Result Part two: ", res)
