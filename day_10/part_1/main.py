import functools
import operator

import fire

POINT_MAP = {")": 3, "]": 57, "}": 1197, ">": 25137}
CORRESPONDING_CHARS = {")": "(", "]": "[", "}": "{", ">": "<"}


def judge_line(line: str) -> int:
    stack = []
    for char in line:
        if char in CORRESPONDING_CHARS.values():
            stack.append(char)
            continue
        if stack.pop() == CORRESPONDING_CHARS[char]:
            continue

        return POINT_MAP[char]
    return 0


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = f.read().splitlines()

    points = functools.reduce(operator.add, map(judge_line, lines))
    print(points)


if __name__ == "__main__":
    fire.Fire(main)
