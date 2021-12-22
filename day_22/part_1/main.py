import timeit

import fire
import numpy as np
from pipe import select


def main(input_file: str = "input.txt") -> None:
    cuboids = parse_input(input_file)

    grid = np.zeros(shape=(101, 101, 101), dtype=int)

    for cuboid in cuboids:
        (x_min, x_max), (y_min, y_max), (z_min, z_max), value = cuboid
        x_min = max(-50, x_min) + 50
        x_max = min(50, x_max) + 50
        y_min = max(-50, y_min) + 50
        y_max = min(50, y_max) + 50
        z_min = max(-50, z_min) + 50
        z_max = min(50, z_max) + 50
        grid[x_min : x_max + 1, y_min : y_max + 1, z_min : z_max + 1] = value

    print(np.sum(grid, axis=None))


def parse_input(input_file: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int], int]]:
    with open(input_file) as f:
        return list(f.read().splitlines() | select(parse_line))


def parse_line(line: str) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], int]:
    on = int(line.startswith("on "))
    line = (
        line.replace("on ", "")
        .replace("off ", "")
        .replace("x=", "")
        .replace("y=", "")
        .replace("z=", "")
        .replace("..", ",")
    )
    x_min, x_max, y_min, y_max, z_min, z_max = map(int, line.split(","))
    return (x_min, x_max), (y_min, y_max), (z_min, z_max), on


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
