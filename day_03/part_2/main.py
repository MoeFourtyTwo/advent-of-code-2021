import functools
import operator

import fire
import numpy as np


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        source_data = np.array([list(x) for x in f.read().splitlines()]).astype(int)

    data = source_data.copy()
    for col_index in range(data.shape[1]):
        one_count = np.sum(data[:, col_index])
        zero_count = len(data) - one_count

        value = int(one_count >= zero_count)

        data = data[data[:, col_index] == value, :]

        if len(data) == 1:
            break

    data = np.squeeze(data)
    oxygen_rating = int(functools.reduce(operator.add, data.astype(int).astype(str)), 2)

    data = source_data.copy()
    for col_index in range(data.shape[1]):
        one_count = np.sum(data[:, col_index])
        zero_count = len(data) - one_count

        value = int(zero_count > one_count)

        data = data[data[:, col_index] == value, :]

        if len(data) == 1:
            break

    data = np.squeeze(data)
    co2_rating = int(functools.reduce(operator.add, data.astype(int).astype(str)), 2)

    print(oxygen_rating * co2_rating)


if __name__ == "__main__":
    fire.Fire(main)
