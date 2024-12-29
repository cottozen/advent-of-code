def convert(input: str):
    blocks = []
    for i in range(0, len(input), 2):
        block_id = i // 2
        num_blocks = int(input[i])
        blocks += [block_id for _ in range(num_blocks)]
        if i < len(input) - 1:
            space = int(input[i + 1])
            blocks += ["." for _ in range(space)]
    return blocks


def move_blocks(blocks: list[str]):
    i, j = blocks.index("."), len(blocks) - 1
    if i == -1:
        return blocks
    while j > i:
        if blocks[i] != ".":
            i += 1
            continue
        blocks[i], blocks[j] = blocks[j], blocks[i]
        j -= 1
    return blocks


def create_space_heap(blocks: list[str]):
    free_space, chunck_start = 0, 0
    space_heap = []
    for i in range(len(blocks)):
        if free_space == 0:
            chunck_start = i
        if blocks[i] == ".":
            free_space += 1
            continue
        if free_space > 0:
            space_heap.append((chunck_start, i))
            free_space = 0
    return space_heap


def move_blocks_part_two(blocks: list[str]):
    space_heap = create_space_heap(blocks)
    block = None
    block_len = 0
    i = len(blocks) - 1
    while i > 0 and len(space_heap):
        if block is None:
            if blocks[i] == ".":
                i -= 1
                continue
            block = blocks[i]
        if blocks[i] == block:
            block_len += 1
            i -= 1
            continue
        for chunk_start, chunck_end in space_heap:
            if chunck_end - chunk_start < block_len:
                continue
            if chunk_start > i:
                break
            blocks[i + 1 : i + block_len + 1] = ["."] * block_len
            blocks[chunk_start : chunk_start + block_len] = [block] * block_len
            break
        # Could make this more efficent by deciding where the heap needs to be updated
        space_heap = create_space_heap(blocks[: i + 1])
        block, block_len = None, 0
    return blocks


def calculate_checksum(blocks: list[str]) -> int:
    res = 0
    for i, b in enumerate(blocks):
        if b != ".":
            res += i * int(b)
    return res


def main():
    with open("input.txt") as file:
        input = file.read().strip()
        blocks = move_blocks(convert(input))
        res = calculate_checksum(blocks)
        print("RESULT: ", res)
        blocks = move_blocks_part_two(convert(input))
        res = calculate_checksum(blocks)
        print("RESULT PART TWO: ", res)


if __name__ == "__main__":
    main()
