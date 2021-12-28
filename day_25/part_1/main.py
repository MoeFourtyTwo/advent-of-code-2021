from __future__ import annotations

import timeit
from contextlib import nullcontext
from io import StringIO

import fire
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import generic_filter


def move(array: np.ndarray) -> int:
    # 0 1 2
    # 3 4 5
    # 6 7 8
    if array[4] == 0:
        if array[3] == 1:
            return 1
        elif array[1] == 2:
            return 2
        else:
            return 0
    elif array[4] == 1:
        if array[5] == 0:
            return 0
        else:
            return 1
    elif array[4] == 2:
        if array[7] == 0 and array[6] != 1:
            return 0
        else:
            return 2


def main(input_file: str = "input.txt", plot: bool = False) -> None:
    with open(input_file) as f:
        input_data = f.read()
    input_data = input_data.replace(".", "0").replace(">", "1").replace("v", "2")

    current_step = np.genfromtxt(StringIO(input_data), dtype=int, delimiter=1)

    iterations = 0
    with plt.ion() if plot else nullcontext():
        if plot:
            plt.axis("off")
            display = plt.imshow(current_step, cmap="magma")
        while True:
            next_step = generic_filter(current_step, move, size=3, mode="wrap")
            if np.array_equal(next_step, current_step):
                break
            current_step = next_step
            iterations += 1
            if plot:
                display.set_data(current_step)
                plt.pause(0.1)
        if plot:
            plt.waitforbuttonpress()
        print(f"{iterations=} ")


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
