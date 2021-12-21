from __future__ import annotations

import dataclasses
import timeit
from typing import Generator

import fire
from pipe import select


def deterministic_die() -> Generator[int, None, None]:
    while True:
        for i in range(1, 101):
            yield i


@dataclasses.dataclass
class Player:
    position: int
    score: int = 0
    throws: int = 0
    board_size: int = 10
    target_score: int = 1000
    simultaneous_throws: int = 3

    def roll(self, die_generator: Generator[int, None, None]) -> bool:
        roll_result = sum(next(die_generator) for _ in range(self.simultaneous_throws))
        self.throws += self.simultaneous_throws
        self.position = (self.position + roll_result) % self.board_size or self.board_size
        self.score += self.position
        return self.score >= self.target_score


def main(input_file: str = "input.txt") -> None:
    positions = parse_input(input_file)

    players = [Player(position) for position in positions]
    die_generator = deterministic_die()

    finished = False
    while not finished:
        for player in players:
            if finished := player.roll(die_generator):
                break

    total_throws = sum(player.throws for player in players)
    loser_score = min(player.score for player in players)

    print(total_throws * loser_score)


def parse_input(input_file: str) -> list[int]:
    with open(input_file) as f:
        return list(f.read().splitlines() | select(lambda row: row.rsplit()[-1]) | select(int))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
