from __future__ import annotations

import dataclasses
import functools
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


@functools.cache
def reachable_nodes(board: Board, node: Node) -> tuple[list[Node], list[int]]:
    targets = []
    distances = []
    for neighbor, distance in zip(node.neighbors(board), node.distances):
        if not neighbor.occupied:
            targets.append(neighbor)
            distances.append(distance)

    for target, distance in zip(targets, distances):
        for neighbor, neighbor_distance in zip(target.neighbors(board), target.distances):
            if neighbor not in targets and not neighbor.occupied and neighbor != node:
                targets.append(neighbor)
                distances.append(distance + neighbor_distance)

    return targets, distances


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
        moves = []
        for from_node in self.grid.values():
            if from_node.has_occupant and not from_node.completed:
                targets, distances = reachable_nodes(self, from_node)

                for to_node, distance in zip(targets, distances):
                    if from_node.is_a_home and not to_node.is_a_home:
                        moves.append((from_node, to_node, distance))

                    if (
                        from_node.is_a_home
                        and to_node.is_a_home
                        and from_node.occupant == to_node.home
                        and all(to_node_occupant == from_node.occupants for to_node_occupant in to_node.occupants)
                    ):
                        moves.append((from_node, to_node, distance))
                    if (
                        not from_node.is_a_home
                        and to_node.home == from_node.occupant
                        and all(to_node_occupant == from_node.occupants for to_node_occupant in to_node.occupants)
                    ):
                        moves.append((from_node, to_node, distance))

        return moves

    def copy(self) -> Board:
        return dataclasses.replace(self, grid=self.grid.copy())

    def __hash__(self):
        return hash((frozenset(self.grid.items())))

    def __str__(self):
        return (
            f"#############\n"
            f"#{self.grid[0].occupants}{self.grid[1].occupants}_{self.grid[2].occupants}_{self.grid[3].occupants}_"
            f"{self.grid[4].occupants}_{self.grid[5].occupants}{self.grid[6].occupants}#\n"
            f"###{self.grid[7].occupants}#{self.grid[9].occupants}#{self.grid[11].occupants}#{self.grid[13].occupants}###\n"
            f"  #########"
        )


@dataclasses.dataclass(frozen=True)
class Node:
    node_id: int
    _neighbors: tuple[int, ...]
    distances: tuple[int, ...]
    home: str = ""
    occupants: str = ""
    max_occupants: int = 1

    def neighbors(self, board: Board) -> tuple[Node, ...]:
        return tuple(board.get_node(node_id) for node_id in self._neighbors)

    @property
    def occupant(self) -> str:
        return self.occupants[0]

    @property
    def at_home(self) -> bool:
        return self.home == self.occupants and self.is_a_home

    @property
    def is_a_home(self) -> bool:
        return self.home != ""

    @property
    def has_occupant(self) -> bool:
        return len(self.occupants) > 0

    @property
    def occupied(self) -> bool:
        return len(self.occupants) == self.max_occupants

    def movable(self, node: Node) -> bool:
        return self.occupied and not node.occupied

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

    @property
    def completed(self) -> bool:
        return self.is_a_home and self.occupied and all(self.home == occupant for occupant in self.occupants)


def initial_state(input_file: str) -> Board:
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
            occupants=starting_configuration[0] + starting_configuration[1],
            max_occupants=2,
        ),
        Node(
            node_id=9,
            _neighbors=(2, 3),
            distances=(2, 2),
            home="B",
            occupants=starting_configuration[2] + starting_configuration[3],
            max_occupants=2,
        ),
        Node(
            node_id=11,
            _neighbors=(3, 4),
            distances=(2, 2),
            home="C",
            occupants=starting_configuration[4] + starting_configuration[5],
            max_occupants=2,
        ),
        Node(
            node_id=13,
            _neighbors=(4, 5),
            distances=(2, 2),
            home="D",
            occupants=starting_configuration[6] + starting_configuration[7],
            max_occupants=2,
        ),
    )
    return board


MIN_COST = 20000
UPPER_BOUND = 20000


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
                else:
                    if total_cost >= min_cost:
                        continue

                    if new_board in known_boards:
                        if total_cost < known_boards[new_board]:
                            known_boards[new_board] = total_cost
                            new_boards[new_board] = total_cost
                    else:
                        known_boards[new_board] = total_cost
                        new_boards[new_board] = total_cost
        open_boards = new_boards


def main(input_file: str = "input.txt") -> None:
    board = initial_state(input_file)
    solve_board(board)


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
