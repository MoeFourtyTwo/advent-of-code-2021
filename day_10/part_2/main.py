import timeit

import fire

POINT_MAP = {c: i for i, c in enumerate(")]}>", start=1)}
CORRESPONDING_CHARS = {")": "(", "]": "[", "}": "{", ">": "<"}
INVERSE_CORRESPONDING_CHARS = {v: k for k, v in CORRESPONDING_CHARS.items()}


def is_valid(line: str) -> bool:
    stack = []
    for char in line:
        if char in CORRESPONDING_CHARS.values():
            stack.append(char)
            continue
        if stack.pop() == CORRESPONDING_CHARS[char]:
            continue

        return False
    return True


def check_missing(line: str) -> int:
    buffer = {c: 0 for c in ")]}>"}
    missing = []

    for char in reversed(line):
        if char in buffer:
            buffer[char] += 1
            continue

        if buffer[INVERSE_CORRESPONDING_CHARS[char]] > 0:
            buffer[INVERSE_CORRESPONDING_CHARS[char]] -= 1
            continue

        missing.append(INVERSE_CORRESPONDING_CHARS[char])

    total = 0
    for char in missing:
        total *= 5
        total += POINT_MAP[char]

    return total


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = f.read().splitlines()

    points = sorted(map(check_missing, filter(is_valid, lines)))

    print(points[len(points) // 2])


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
