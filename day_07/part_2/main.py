import fire
import numpy as np
from matplotlib import pyplot as plt
from tqdm import trange


def calculate_cost(data: np.ndarray, target_position: int) -> float:
    distances = np.abs(data - target_position)
    costs = distances * (distances + 1) / 2
    return float(np.sum(costs))


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        data = np.array(f.read().split(","), dtype=int)

    min_pos = int(np.mean(data))
    cost = calculate_cost(data, min_pos)
    print(cost)

    costs = [calculate_cost(data, i) for i in trange(min(data), max(data))]
    plt.plot(costs)
    plt.show()

    print(np.min(costs))
    print(np.argmin(costs))


if __name__ == "__main__":
    fire.Fire(main)
