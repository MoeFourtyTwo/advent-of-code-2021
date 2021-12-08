import functools
import operator
from collections import Counter
from typing import Iterable

import fire

NUMBER_MAPPING = {
    pattern: str(idx)
    for idx, pattern in enumerate(
        [
            frozenset("abcefg"),
            frozenset("cf"),
            frozenset("acdeg"),
            frozenset("acdfg"),
            frozenset("bcdf"),
            frozenset("abdfg"),
            frozenset("abdefg"),
            frozenset("acf"),
            frozenset("abcdefg"),
            frozenset("abcdfg"),
        ]
    )
}
FILTER_MAP = {
    "a": ({2, 4}, 8),
    "b": (set(), 6),
    "c": ({5}, 6),
    "d": ({4}, 6),
    "e": (set(), 4),
    "f": (set(), 9),
    "g": ({6}, 4),
}


def count_chars(patterns: Iterable[set[str]]) -> dict[int, str]:
    counts = functools.reduce(
        operator.add,
        map(Counter, patterns),
    )
    return {v: k for k, v in counts.items()}


def find_mapping(patterns: list[set[str]]) -> dict[str, str]:
    mapping = {}
    for char, (filter_set, count) in FILTER_MAP.items():
        filtered_patterns = filter(lambda p: len(p) not in filter_set, patterns)
        counts = count_chars(filtered_patterns)
        mapping[counts[count]] = char
    return mapping


def get_number_str(code: str) -> str:
    return NUMBER_MAPPING[frozenset(code)]


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = f.read().splitlines()

    lines = [(list(map(set, left.split(" "))), right) for left, right in [line.split(" | ") for line in lines]]

    total = 0
    for pattern, code in lines:
        mapping = find_mapping(pattern)

        translated = "".join(map(lambda c: mapping.get(c, " "), code))

        number_str = ""
        for translated_part in translated.split(" "):
            number_str += get_number_str(translated_part)
        total += int(number_str)

    print(total)


if __name__ == "__main__":
    fire.Fire(main)
