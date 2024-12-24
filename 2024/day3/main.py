import enum


def get_input() -> str:
    with open("input.txt", "r") as file:
        text = file.read()
        return text


class Token(enum.StrEnum):
    MUL = "mul"
    OPEN = "("
    CLOSE = ")"
    COMMA = ","
    DONT = "don't()"
    DO = "do()"
    # X is a placeholder for all other invalid chars
    INVALID = "X"


type MulSequence = list[Token | str]

VALID_SEQ = [Token.MUL, Token.OPEN, str, Token.COMMA, str, Token.CLOSE]
SEQ_LEN = len(VALID_SEQ)


def compare_token(token: Token, i: int, text: str):
    token_len = len(token)
    return i + token_len < len(text) and text[i : i + token_len] == token


def tokenize(text: str) -> MulSequence:
    tokens: MulSequence = []
    i = 0
    while i < len(text):
        increment = 1
        if compare_token(Token.DONT, i, text):
            tokens.append(Token.DONT)
            increment = len(Token.DONT)
        elif compare_token(Token.DO, i, text):
            tokens.append(Token.DO)
            increment = len(Token.DO)
        elif compare_token(Token.MUL, i, text):
            tokens.append(Token.MUL)
            increment = len(Token.MUL)
        elif text[i] == Token.OPEN:
            tokens.append(Token.OPEN)
        elif text[i].isdigit():
            prev_num = tokens[-1]
            if prev_num.isdigit() and len(prev_num) < 3:
                tokens[-1] += text[i]
            else:
                tokens.append(text[i])
        elif text[i] == Token.COMMA:
            tokens.append(Token.COMMA)
        elif text[i] == Token.CLOSE:
            tokens.append(Token.CLOSE)
        else:
            tokens.append(Token.INVALID)
        i += increment
    return tokens


def parse(tokens: MulSequence) -> int:
    result = 0
    seq_index = 0
    disabled = False
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == Token.DONT:
            disabled = True
        if t == Token.DO:
            disabled = False
        if disabled:
            i += 1
            continue
        if t != Token.INVALID and (
            (type(t) is str and len(t) < 4 and len(t) > 0) or t == VALID_SEQ[seq_index]
        ):
            seq_index += 1
        else:
            # Check if its start of new valid mul
            seq_index = int(t == VALID_SEQ[0])
        if seq_index == SEQ_LEN:
            # Get digits in sequence by index
            result += int(tokens[i + 3 - SEQ_LEN]) * int(tokens[i + 5 - SEQ_LEN])
            seq_index = 0
        i += 1
    return result


if __name__ == "__main__":
    text = get_input()
    res = parse(tokenize(text))
    print("Result: ", res)
