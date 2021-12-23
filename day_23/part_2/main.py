from __future__ import annotations

import dataclasses
import functools
import operator
import random
import timeit
from typing import Optional

import fire
from pipe import select
from tqdm import tqdm

COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def check_move_from_home(source: Node, target: Node) -> bool:
    return not target.is_a_home or check_move_into_home(source, target)


def check_move_into_home(source: Node, target: Node) -> bool:
    return target.is_a_home and source.occupant == target.home and target.all_occupants_from_home


def reachable_nodes(board: Board, source: Node) -> list[tuple[Node, Node, int]]:
    targets_with_distances = source.get_relevant_neighbors_with_distance(board)

    for target, distance in targets_with_distances:
        for neighbor, neighbor_distance in target.get_relevant_neighbors_with_distance(board):
            if neighbor != source and all(neighbor != added for added, _ in targets_with_distances):
                targets_with_distances.append((neighbor, neighbor_distance + distance))

    return trim(source, targets_with_distances)


def trim(source: Node, targets_with_distances: list[tuple[Node, int]]) -> list[tuple[Node, Node, int]]:
    check_func = check_move_from_home if source.is_a_home else check_move_into_home
    output = []
    for target, distance in targets_with_distances:
        if check_func(source, target):
            output.append((source, target, distance))
    return output


@dataclasses.dataclass
class Board:
    grid: dict[int, Node] = dataclasses.field(default_factory=dict)

    def add_nodes(self, *nodes: Node) -> None:
        for node in nodes:
            self.add_node(node)

    def add_node(self, node: Node) -> None:
        self.grid[node.node_id] = node

    def get_node(self, node_id: int) -> Node:
        return self.grid[node_id]

    def move_occupant(self, from_node: Node, to_node: Node, distance: int) -> tuple[Board, int]:
        new_board = self.copy()
        new_board.grid[from_node.node_id], occupant, extra_from_dist = from_node.pop()
        new_board.grid[to_node.node_id], extra_to_dist = to_node.push(occupant)
        move_cost = COSTS[occupant] * (extra_from_dist + distance + extra_to_dist)
        return new_board, move_cost

    @property
    def completed(self) -> bool:
        for node in self.grid.values():
            if node.is_a_home:
                if any(node.home != occupant for occupant in node.occupants):
                    return False
            elif node.occupied:
                return False
        return True

    def generate_moves(self) -> list[tuple[Node, Node, int]]:
        return functools.reduce(
            operator.add,
            [
                reachable_nodes(self, from_node)
                for from_node in self.grid.values()
                if from_node.has_occupant and not from_node.completed
            ],
        )

    def copy(self) -> Board:
        return dataclasses.replace(self, grid=self.grid.copy())

    def __hash__(self):
        return hash((frozenset(self.grid.items())))


@dataclasses.dataclass(frozen=True)
class Node:
    node_id: int
    _neighbors: tuple[int, ...]
    distances: tuple[int, ...]
    home: str = ""
    occupants: str = ""
    max_occupants: int = 1

    def get_relevant_neighbors_with_distance(self, board: Board) -> list[tuple[Node, int]]:
        return [
            (board.get_node(node_id), distance)
            for node_id, distance in zip(self._neighbors, self.distances)
            if not board.get_node(node_id).occupied
        ]

    @property
    def occupant(self) -> str:
        return self.occupants[0]

    @property
    def is_a_home(self) -> bool:
        return self.home != ""

    @property
    def has_occupant(self) -> bool:
        return len(self.occupants) > 0

    @property
    def occupied(self) -> bool:
        return len(self.occupants) == self.max_occupants

    @property
    def all_occupants_from_home(self) -> bool:
        return all(self.occupant == occupant for occupant in self.occupants[1:])

    @property
    def completed(self) -> bool:
        return self.is_a_home and self.occupied and all(self.home == occupant for occupant in self.occupants)

    def __hash__(self):
        return hash((self.node_id, self.occupants))

    def __str__(self):
        return f"{self.node_id} {self.occupants}"

    def pop(self) -> tuple[Node, str, int]:
        assert len(self.occupants) > 0
        first_occupant = self.occupants[0]
        remaining_occupants = self.occupants[1:]
        return (
            dataclasses.replace(self, occupants=remaining_occupants),
            first_occupant,
            self.max_occupants - len(self.occupants),
        )

    def push(self, occupant: str) -> tuple[Node, int]:
        assert len(self.occupants) < self.max_occupants
        return (
            dataclasses.replace(self, occupants=occupant + self.occupants),
            self.max_occupants - len(self.occupants) - 1,
        )


def initial_state(input_file: str, part_2: bool = True) -> Board:
    with open(input_file) as f:
        starting_configuration = [char for char in f.read() if char in "ABCD"]
        starting_configuration = "".join(
            "".join(pair) for pair in zip(starting_configuration[:4], starting_configuration[4:])
        )

    board = Board()
    board.add_nodes(
        Node(node_id=0, _neighbors=(1,), distances=(1,)),
        Node(node_id=1, _neighbors=(0, 2, 7), distances=(1, 2, 2)),
        Node(node_id=2, _neighbors=(1, 3, 7, 9), distances=(2, 2, 2, 2)),
        Node(node_id=3, _neighbors=(2, 4, 9, 11), distances=(2, 2, 2, 2)),
        Node(node_id=4, _neighbors=(3, 5, 11, 13), distances=(2, 2, 2, 2)),
        Node(node_id=5, _neighbors=(4, 6, 13), distances=(2, 1, 2)),
        Node(node_id=6, _neighbors=(5,), distances=(1,)),
        Node(
            node_id=7,
            _neighbors=(1, 2),
            distances=(2, 2),
            home="A",
            occupants=starting_configuration[0] + ("DD" if part_2 else "") + starting_configuration[1],
            max_occupants=4 if part_2 else 2,
        ),
        Node(
            node_id=9,
            _neighbors=(2, 3),
            distances=(2, 2),
            home="B",
            occupants=starting_configuration[2] + ("CB" if part_2 else "") + starting_configuration[3],
            max_occupants=4 if part_2 else 2,
        ),
        Node(
            node_id=11,
            _neighbors=(3, 4),
            distances=(2, 2),
            home="C",
            occupants=starting_configuration[4] + ("BA" if part_2 else "") + starting_configuration[5],
            max_occupants=4 if part_2 else 2,
        ),
        Node(
            node_id=13,
            _neighbors=(4, 5),
            distances=(2, 2),
            home="D",
            occupants=starting_configuration[6] + ("AC" if part_2 else "") + starting_configuration[7],
            max_occupants=4 if part_2 else 2,
        ),
    )
    return board


MIN_COST = 100000


def solve_board(board: Board):
    known_boards = {board: 0}
    min_cost = MIN_COST
    open_boards = {board: 0}

    completions = 0
    while open_boards:
        new_boards = {}
        t = tqdm(open_boards.items())
        t.set_description(f"Open: {len(open_boards): >10}, Completed: {completions: >10}, Min: {min_cost: >10}")
        for board, current_cost in t:
            moves = board.generate_moves()
            sorted(moves, key=operator.itemgetter(2), reverse=True)

            for from_node, to_node, distance in moves:
                new_board, additional_cost = board.move_occupant(from_node, to_node, distance)
                total_cost = current_cost + additional_cost

                if new_board.completed:
                    if total_cost < min_cost:
                        min_cost = total_cost
                        completions += 1
                        t.set_description(
                            f"Open: {len(open_boards): >10}, Completed: {completions: >10}, Min: {min_cost: >10}"
                        )
                elif total_cost >= min_cost:
                    continue
                elif new_board not in known_boards or total_cost < known_boards[new_board]:
                    known_boards[new_board] = total_cost
                    new_boards[new_board] = total_cost
        open_boards = new_boards


def main(input_file: str = "input.txt") -> None:
    board = initial_state(input_file)

    solve_board(board)


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
