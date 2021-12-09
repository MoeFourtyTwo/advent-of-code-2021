import fire
import numpy as np


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

    total = np.sum(data[result] + 1)
    print(total)


if __name__ == "__main__":
    fire.Fire(main)
