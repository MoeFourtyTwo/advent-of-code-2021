import time
import timeit
from contextlib import nullcontext

import fire
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange


def main(input_file: str = "input.txt", plot: bool = False) -> None:
    data = np.genfromtxt(input_file, dtype=int, delimiter=1)

    if plot:
        cm = plt.ion()
    else:
        cm = nullcontext()

    with cm:
        if plot:
            plt.axis("off")
        total_flashes = 0

        if plot:
            t = plt.text(0, -1, f"{total_flashes=}", fontsize=10, color="red")
            image = plt.imshow(data, cmap="magma")

        for iteration in trange(100):
            data, new_flashes = next_iteration(data)
            total_flashes += new_flashes

            if plot:
                image.set_data(data)
                t.set_text(f"{total_flashes=} {iteration=}")
                plt.pause(0.001)

            if np.all(data == 0):
                break

        print(f"{total_flashes=}")


def next_iteration(data: np.array) -> tuple[np.ndarray, int]:
    flashed = np.zeros(data.shape, dtype=bool)
    data += 1
    plt.pause(0.1)
    flashed[data > 9] = True
    # noinspection PyTypeChecker
    to_process: list[tuple[int, int]] = list(zip(*np.where(flashed)))
    while to_process:
        x, y = to_process.pop(0)
        data[max(x - 1, 0) : min(x + 2, 10), max(y - 1, 0) : min(y + 2, 10)] += 1
        new_flashes = (data > 9) & ~flashed
        to_process.extend(zip(*np.where(new_flashes)))
        flashed |= new_flashes
    data[flashed] = 0
    return data, int(np.sum(flashed))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
