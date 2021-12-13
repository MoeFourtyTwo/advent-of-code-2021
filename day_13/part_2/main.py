import timeit
from operator import itemgetter

import fire
import numpy as np


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = f.read().splitlines()

    points = []
    folds = []
    for line in lines:
        if not line:
            continue

        if line[0].isdigit():
            points.append(tuple(map(int, line.split(","))))
        if line.startswith("fold along "):
            axis, place = line.replace("fold along ", "").split("=")
            folds.append((axis, int(place)))

    x_max, y_max = max(map(itemgetter(0), points)), max(map(itemgetter(1), points))

    grid = np.zeros((x_max + 1, y_max + 1), dtype=bool)
    for point in points:
        grid[point] = 1

    for axis, place in folds:
        if axis == "x":
            left, right = grid[:place, :], grid[place + 1 :, :]

            grid = left + np.flip(right, axis=0)

        else:
            top, bot = grid[:, :place], grid[:, place + 1 :]
            grid = top + np.flip(bot, axis=1)

        break

    print(np.sum(grid))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
