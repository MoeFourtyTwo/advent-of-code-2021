import functools
import operator

import fire
import numpy as np


def main():
    with open('input.txt') as f:
        data = np.array([list(x) for x in f.read().splitlines()]).astype(int)

    sums = np.sum(data, axis=0)

    counts = sums > len(data) / 2
    gamma = int(functools.reduce(operator.add, counts.astype(int).astype(str)), 2)
    epsilon = int(functools.reduce(operator.add, (~counts).astype(int).astype(str)), 2)

    print(gamma * epsilon)


if __name__ == '__main__':
    fire.Fire(main)
