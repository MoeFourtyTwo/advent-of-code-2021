import timeit

import fire
import networkx as nx
import numpy as np


def main(input_file: str = "input.txt") -> None:
    data = np.genfromtxt(input_file, dtype=int, delimiter=1)
    data = np.pad(data, ((1, 1), (1, 1)), mode="constant", constant_values=0)

    G = nx.DiGraph()

    for i in range(len(data)):
        for j in range(len(data[1])):
            G.add_node(f"{i},{j}")

    for i in range(1, len(data) - 1):
        for j in range(1, len(data[1]) - 1):
            for k, l in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                G.add_edge(f"{i},{j}", f"{i + k},{j + l}", weight=data[i + k][j + l])

    print(nx.shortest_path_length(G, source="1,1", target=f"{len(data) - 2},{len(data) - 2}", weight="weight"))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
