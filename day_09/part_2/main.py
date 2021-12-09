import dataclasses
import functools
import operator

import fire
import numpy as np


@dataclasses.dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def is_valid(self, grid: np.ndarray) -> bool:
        return 0 <= self.x < grid.shape[0] and 0 <= self.y < grid.shape[1]


@dataclasses.dataclass
class Basin:
    center: Point
    container: set[Point] = dataclasses.field(default_factory=set)

    def __post_init__(self):
        self.container.add(self.center)

    @property
    def size(self):
        return len(self.container)

    def grow(self, grid: np.ndarray):
        queue = [self.center]

        while queue:
            point = queue.pop(0)
            for offset in [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]:
                candidate = point + offset
                if candidate.is_valid(grid) and grid[candidate.x, candidate.y] != 9 and candidate not in self.container:
                    self.container.add(candidate)
                    queue.append(candidate)


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = f.read().splitlines()

    data = np.array([list(line) for line in lines], dtype=np.int8)

    col = np.full((len(data), 1), 10, dtype=np.int8)
    row = np.full((1, len(data)), 10, dtype=np.int8)

    shift_up = np.concatenate((data[1:, :], row))
    shift_down = np.concatenate((row, data[:-1, :]))

    shift_left = np.concatenate((data[:, 1:], col), axis=-1)
    shift_right = np.concatenate((col, data[:, :-1]), axis=-1)

    result = np.logical_and(
        np.logical_and((shift_down - data) > 0, (shift_up - data) > 0),
        np.logical_and((shift_right - data) > 0, (shift_left - data) > 0),
    )

    low_points = np.where(result)

    sizes = []
    for x, y in zip(*low_points):
        basin = Basin(center=Point(x, y))
        basin.grow(data)
        sizes.append(basin.size)

    print(functools.reduce(operator.mul, sorted(sizes, reverse=True)[:3]))


if __name__ == "__main__":
    fire.Fire(main)
