import timeit
from collections import defaultdict

import fire


def search(
    graph: dict[str, list[str]], current: str, current_path: list[str], has_visited_twice: bool
) -> list[list[str]]:
    current_path.append(current)
    if current == "end":
        return [current_path]

    paths = []
    for node in graph[current]:
        if node not in current_path or node.isupper():
            paths.extend(search(graph, node, current_path.copy(), has_visited_twice))
        if node in current_path and node.islower() and not has_visited_twice:
            paths.extend(search(graph, node, current_path.copy(), True))

    return paths


def parse_graph(data: list[str]) -> dict[str, list[str]]:
    graph = defaultdict(list)
    for line in data:
        node_a, node_b = line.split("-")

        if node_a != "end" and node_b != "start":
            graph[node_a].append(node_b)
        if node_b != "end" and node_a != "start":
            graph[node_b].append(node_a)
    return graph


def main(input_file: str = "input.txt") -> None:

    with open(input_file) as f:
        data = f.read().splitlines()

    graph = parse_graph(data)

    paths = search(graph, "start", [], False)
    print(len(paths))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
