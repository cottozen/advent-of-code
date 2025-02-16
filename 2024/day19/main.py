import functools

FILE_PATH = "input.txt"


def parse_input():
    with open(FILE_PATH, "r") as file:
        lines = file.readlines()
        towels = [t.strip() for t in lines[0].split(",")]
        patterns = [p.strip() for p in lines[2:]]
    return towels, patterns


def solve_pattern(towels: list[str], pattern: str) -> int:
    @functools.cache
    def search(curr: str):
        if not pattern.startswith(curr) or len(curr) > len(pattern):
            return False
        if curr == pattern:
            return True
        return sum(search(curr + t) for t in towels)

    return search("")


def solve_patterns(towels: list[str], patterns: list[str]):
    solutions = [solve_pattern(towels, p) for p in patterns]
    return sum(s > 0 for s in solutions), sum(solutions)


def main():
    towels, patterns = parse_input()
    res1, res2 = solve_patterns(towels, patterns)
    print("RESULT: ", res1)
    print("RESULT PART TWO: ", res2)


if __name__ == "__main__":
    main()
