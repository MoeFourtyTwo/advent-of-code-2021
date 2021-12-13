import timeit
from operator import itemgetter

import fire
import numpy as np
from matplotlib import pyplot as plt


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
            if left.shape[0] > right.shape[0]:
                right = np.concatenate(
                    [right, np.zeros((left.shape[0] - right.shape[0], right.shape[1]), dtype=bool)], axis=0
                )
            if left.shape[0] < right.shape[0]:
                left = np.concatenate(
                    [np.zeros((right.shape[0] - left.shape[0], right.shape[1]), dtype=bool), left], axis=0
                )

            grid = left + np.flip(right, axis=0)

        else:
            top, bot = grid[:, :place], grid[:, place + 1 :]
            if top.shape[1] > bot.shape[1]:
                bot = np.concatenate([bot, np.zeros((bot.shape[0], top.shape[1] - bot.shape[1]), dtype=bool)], axis=1)
            if top.shape[1] < bot.shape[1]:
                top = np.concatenate([np.zeros((bot.shape[0], bot.shape[1] - top.shape[1]), dtype=bool), top], axis=1)
            grid = top + np.flip(bot, axis=1)

    plt.imshow(np.transpose(grid))
    plt.show()

    print(np.sum(grid))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
