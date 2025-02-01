from typing import Callable, TypedDict


class Registers(TypedDict):
    A: int
    B: int
    C: int


def replace_bits(num: int, pos: int, mask: int):
    num_bits = num.bit_length()
    pos_shift = num_bits - pos - 3
    filled_mask = ((1 << num_bits) - 1) & ~(0b111 << pos_shift)
    return (num & filled_mask) | (mask << pos_shift)


class Program:

    def __init__(self, registers: Registers, instructions: list[int]) -> None:
        self.instructions = instructions
        self._initial_registers = registers
        self._memo = {}
        self.reset()

    def reset(self):
        self.pointer = 0
        self._jumped = False
        self.outputs = []
        self.registers = {**self._initial_registers}

    def adv(self, operand: int):
        numerator = self.registers["A"]
        combo = self.get_combo(operand)
        denominator: int = 2**combo
        res = numerator // denominator
        self.registers["A"] = res

    def bxl(self, operand: int):
        res = self.registers["B"] ^ operand
        self.registers["B"] = res

    def bst(self, operand: int):
        res = self.get_combo(operand) % 8
        self.registers["B"] = res

    def jnz(self, operand: int):
        if self.registers["A"] == 0:
            return
        self.pointer = operand
        self._jumped = True

    def bxc(self, operand: int):
        res = self.registers["B"] ^ self.registers["C"]
        self.registers["B"] = res

    def out(self, operand: int):
        res = self.get_combo(operand) % 8
        self.outputs.append(res)

    def bdv(self, operand: int):
        numerator = self.registers["A"]
        denominator: int = 2 ** self.get_combo(operand)
        res = numerator // denominator
        self.registers["B"] = res

    def cdv(self, operand: int):
        numerator = self.registers["A"]
        denominator: int = 2 ** self.get_combo(operand)
        res = numerator // denominator
        self.registers["C"] = res

    def get_combo(self, operand: int) -> int:
        match operand:
            case 4:
                return self.registers["A"]
            case 5:
                return self.registers["B"]
            case 6:
                return self.registers["C"]
            case _:
                return operand

    def fix_program(self, bit_len: int):
        a_init: int = 2**bit_len
        bit_masks = [0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
        valid_bit_masks: list[int] = []

        def dfs(a: int, pos: int):
            if self.execute(a) == self.instructions:
                valid_bit_masks.append(a)
                return
            if a.bit_length() - pos < 3:
                return
            valid = []
            num_elemets = pos // 3 + 1
            for mask in bit_masks:
                a_new = replace_bits(a, pos, mask)
                outputs = self.execute(a_new)
                if outputs[-num_elemets:] == self.instructions[-num_elemets:]:
                    valid.append(a_new)
            for a in valid:
                dfs(a, pos + 3)

        dfs(a_init, 0)
        return valid_bit_masks

    def execute(self, a_init: int) -> list[int]:
        self.reset()
        self.registers["A"] = a_init
        if outputs := self._memo.get(a_init):
            self.outputs = outputs
            return self.outputs

        OPCODE_MAPPING: dict[int, Callable[[int], None]] = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,  # Jump
            4: self.bxc,
            5: self.out,  # Out
            6: self.bdv,
            7: self.cdv,
        }

        self.pointer = 0

        curr_a = self.registers["A"]
        while self.pointer < len(self.instructions):
            opcode = self.instructions[self.pointer]
            operand = self.instructions[self.pointer + 1]
            operation = OPCODE_MAPPING[opcode]
            operation(operand)
            if curr_a != self.registers["A"]:
                curr_a = self.registers["A"]
            if self._jumped:
                self._jumped = False
                continue
            self.pointer += 2
        self._memo[a_init] = self.outputs
        return self.outputs


def parse_program(program: str) -> Program:
    lines = program.split("\n")
    registers: Registers = {"A": 0, "B": 0, "C": 0}
    for reg in lines[0:3]:
        [_, reg, value] = reg.split(" ")
        registers[reg[0:1]] = int(value)
    return Program(
        registers, [int(i) for i in lines[-1].removeprefix("Program: ").split(",")]
    )


def solve(program: Program):
    num_bits = 0
    outputs = []
    bit_range = []
    while len(outputs) <= len(program.instructions):
        num_bits += 1
        outputs = program.execute(2**num_bits)
        if len(outputs) == len(program.instructions):
            bit_range.append(num_bits)

    valid_outputs = []
    for num_bits in bit_range:
        valid_outputs += program.fix_program(num_bits)
    valid_outputs.sort()
    print(bit_range)
    print("ANSWER IS: ", min(valid_outputs))

    solve(program)


def main():
    with open("input.txt") as file:
        program = parse_program(file.read().strip())
        solve(program)


if __name__ == "__main__":
    main()
