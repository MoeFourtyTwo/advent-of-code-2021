import fire
import numpy as np


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        data = [int(x) for x in f.read().splitlines()]

    array = np.array(data)
    sums = np.sum(np.lib.stride_tricks.sliding_window_view(array, 3), axis=1)
    count = sum(cur > prev for prev, cur in zip(sums[:-1], sums[1:]))

    print(count)


if __name__ == "__main__":
    fire.Fire(main)
