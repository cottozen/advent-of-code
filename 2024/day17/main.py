from typing import Callable, DefaultDict, TypedDict


class Registers(TypedDict):
    A: int
    B: int
    C: int


def replace_bits(num: int, pos: int, mask: int, num_bits: int):
    pos_shift = num_bits - min((pos + 3), 17)
    filled_mask = ((1 << num_bits) - 1) & ~(
        0b111 << pos_shift
    )  # Ensure 17-bit mask and cleat the first 3 bits
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
        backtrack = DefaultDict(set)
        a = 2**bit_len
        instruction_index = len(self.instructions)
        while self.instructions != self.outputs:
            bit_masks = [0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
            pos_shift = (len(self.instructions) - instruction_index) * 3

            def is_correct_output():
                return (
                    len(self.outputs)
                    and self.outputs[instruction_index::]
                    == self.instructions[instruction_index::]
                )

            for mask in bit_masks:
                self.reset()
                if mask in backtrack[pos_shift]:
                    continue
                backtrack[pos_shift].add(mask)
                new_a = replace_bits(a, pos_shift, mask, bit_len + 1)
                self.registers["A"] = new_a
                self.execute()
                if is_correct_output():
                    instruction_index -= 1
                    a = new_a
                    break
            else:
                if pos_shift == 0:
                    print("A: ", bin(a))
                    print("outputs: ", self.outputs)
                    print("attemps: ", backtrack)
                    raise Exception("Cannot backtrack from here")
                # backtrack
                print(
                    f"backtracking from pos_shift={pos_shift} and instruction_index={instruction_index}"
                )
                backtrack[pos_shift] = set()
                instruction_index += 1
        return a, self.outputs

    def execute(self) -> list[int]:
        start_a = self.registers["A"]
        if outputs := self._memo.get(start_a):
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
                # print(bin(curr_a))
            if self._jumped:
                self._jumped = False
                continue
            self.pointer += 2
        self._memo[start_a] = self.outputs
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


def test():
    # x = 2024
    x = 2024
    example = f"""Register A: {x}
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

    program = parse_program(example)
    print("INSTRUCTIONS: ", program.instructions)
    print("TARGET: ", bin(117440))
    bit_len = (len(program.instructions) * 3) - 2
    print(program.fix_program(bit_len))
    print("NUM TRIES:", len(program._memo))


def main():
    with open("input.txt") as file:
        program = parse_program(file.read().strip())
        # bit_len = 45
        # outputs = program.fix_program(bit_len)

        num_bits = 0
        outputs = program.execute()
        while len(outputs) != len(program.instructions):
            num_bits += 1
            program.reset()
            program.registers["A"] = 2**num_bits
            outputs = program.execute()

        min_a = 2**num_bits
        print(num_bits)
        print(bin(min_a))

        a = min_a
        while outputs != program.instructions:
            a += 1
            program.reset()
            program.registers["A"] = a
            outputs = program.execute()
            print(outputs)
        print("A: ", a)


if __name__ == "__main__":

    # test()
    main()
