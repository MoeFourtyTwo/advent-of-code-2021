from __future__ import annotations

import contextlib
import timeit
from collections import Callable
from contextlib import nullcontext
from io import StringIO

import fire
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve

KERNEL = np.array([[1, 2, 4], [8, 16, 32], [64, 128, 256]])


def main(input_file: str = "input.txt", plot: bool = False, iterations: int = 50) -> None:
    image_enhancement_algorithm, image = parse_input(input_file)

    if plot:
        cm = plt.ion()
    else:
        cm = nullcontext()

    with cm:
        if plot:
            plt.axis("off")
            plt_image = plt.imshow(image, cmap="gray")
            plt.waitforbuttonpress()

        background = 0
        for _ in range(iterations):
            image, background = iterate(image, image_enhancement_algorithm, background=background)

            if plot:
                plt_image.set_data(image)
                plt.pause(0.1)

        print(f"Total lights: {np.sum(image, axis=None)}")
        if plot:
            plt.waitforbuttonpress()


def iterate(image: np.ndarray, image_enhancement_algorithm: np.ndarray, background: int = 0) -> tuple[np.ndarray, int]:
    new_background = image_enhancement_algorithm[0 if background == 0 else -1]
    image = np.pad(image, 1, "constant", constant_values=background)

    image = image_enhancement_algorithm[convolve(image, KERNEL, mode="constant", cval=background)]
    return image, new_background


def parse_input(input_file: str) -> tuple[np.ndarray, np.ndarray]:
    with open(input_file) as f:
        rows = f.read().replace(".", "0").replace("#", "1").splitlines()

    image_enhancement_algorithm, _, *image = rows
    image_enhancement_algorithm = np.array(list(image_enhancement_algorithm), dtype=int)

    image = np.genfromtxt(StringIO("\n".join(image)), dtype=int, delimiter=1)
    image = np.pad(image, 1, "constant", constant_values=0)

    return image_enhancement_algorithm, image


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
