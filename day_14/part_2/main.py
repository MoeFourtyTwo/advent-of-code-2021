import timeit
from collections import Counter

import fire


def main(input_file: str = "input.txt") -> None:
    template, substitutions = parse_input(input_file)

    counter = Counter()
    for combination in zip(template, template[1:]):
        counter["".join(combination)] += 1

    for _ in range(40):
        next_counter = counter.copy()
        for combination, count in counter.items():
            if count > 0 and combination in substitutions:
                to_str = substitutions[combination]
                next_counter[combination] -= count
                next_counter[combination[0] + to_str] += count
                next_counter[to_str + combination[1]] += count
        counter = next_counter

    char_counter = Counter()
    for combination, count in counter.items():
        for char in combination:
            char_counter[char] += count

    char_counter[template[0]] += 1
    char_counter[template[-1]] += 1
    char_counter = {char: count // 2 for char, count in char_counter.items()}

    print(max(char_counter.values()) - min(char_counter.values()))


def parse_input(input_file: str) -> tuple[str, dict[str, str]]:
    with open(input_file) as f:
        lines = f.read().splitlines()
    template, _, *substitutions = lines
    substitutions = {
        from_str: to_str for from_str, to_str in [substitution.split(" -> ") for substitution in substitutions]
    }
    return template, substitutions


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
