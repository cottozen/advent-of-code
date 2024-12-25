from typing import cast


def process_update(rules: dict[str, list[str]], update: list[str]) -> None | int:
    update_index = {n: i for i, n in enumerate(update)}
    for i, n in enumerate(update):
        if n not in rules:
            continue
        for c in rules[n]:
            index = update_index.get(c)
            # if index is None the rule dosent apply since page number isnt in the update
            # if the condition is not before the page number as required by the rule then its not valid
            if index is not None and index > i:
                return None
    return int(update[len(update) // 2])


def process_update_with_fixes(
    rules: dict[str, list[str]], update: list[str]
) -> None | int:
    update_index = {n: i for i, n in enumerate(update)}
    had_error = False
    i = 0
    while i < len(update):
        n = update[i]
        if n not in rules:
            i += 1
            continue
        for c in rules[n]:
            index = update_index.get(c)
            if index is not None and index > i:
                had_error = True
                # fix it
                update[index], update[i] = update[i], update[index]
                update_index[c], update_index[n] = i, index
                # substract one to nullify the increment below
                i -= 1
                break
        i += 1
    return int(update[len(update) // 2]) if had_error else None


def solve_part_two(lines: list[str]) -> int:
    rules = {}
    result = 0
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if "|" in line:
            condition = line.split("|")
            first, second = condition[0], condition[1]
            if second not in rules:
                rules[second] = []
            rules[second].append(first)
            continue
        update = cast(list[str], line.split(","))
        if middle_page_num := process_update_with_fixes(rules, update):
            result += middle_page_num
    return result


def solve_part_one(lines: list[str]) -> int:
    rules = {}
    result = 0
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if "|" in line:
            condition = line.split("|")
            first, second = condition[0], condition[1]
            if second not in rules:
                rules[second] = []
            rules[second].append(first)
            continue
        if middle_page_num := process_update(rules, line.split(",")):
            result += middle_page_num
    return result


def main():
    with open("input.txt", "r") as file:
        lines = file.readlines()
    result = solve_part_one(lines)
    print("Result=", result)
    result = solve_part_two(lines)
    print("Result part two=", result)


if __name__ == "__main__":
    main()
