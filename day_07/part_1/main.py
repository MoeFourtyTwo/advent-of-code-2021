import fire
import numpy as np
from matplotlib import pyplot as plt
from tqdm import trange


def calculate_cost(data: np.ndarray, target_position: int) -> int:
    return int(np.sum(np.abs(data - target_position)))


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        data = np.array(f.read().split(","), dtype=int)

    min_pos = int(np.median(data))
    cost = calculate_cost(data, min_pos)
    print(cost)

    costs = [calculate_cost(data, i) for i in trange(min(data), max(data))]
    plt.plot(costs)
    plt.show()


if __name__ == "__main__":
    fire.Fire(main)
