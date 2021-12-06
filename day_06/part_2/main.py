from collections import Counter

import fire


def next_step(data: dict) -> dict:
    next_data = {k - 1: v for k, v in data.items()}
    next_data[8] = next_data.get(-1, 0)
    next_data[6] = next_data.get(6, 0) + next_data.get(-1, 0)
    if -1 in next_data:
        del next_data[-1]
    return next_data


def main(generation_count: int = 256) -> None:
    with open('input.txt') as f:
        data = Counter(map(int, f.read().split(',')))

    for _ in range(generation_count):
        data = next_step(data)

    print(sum(data.values()))


if __name__ == '__main__':
    fire.Fire(main)
