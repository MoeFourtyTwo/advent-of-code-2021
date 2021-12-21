from __future__ import annotations

import dataclasses
import functools
import itertools
import timeit
from collections import defaultdict, Counter

import fire
from pipe import select

TARGET_SCORE = 21
BOARD_SIZE = 10
TOTAL_DICE = 3
DIE_FACES = 3
POSSIBLE_RESULTS = Counter(sum(r) for r in itertools.product(range(1, DIE_FACES + 1), repeat=TOTAL_DICE))


@functools.cache
def move(position: int, roll_result: int) -> int:
    return (position + roll_result) % BOARD_SIZE or BOARD_SIZE


@dataclasses.dataclass(frozen=True)
class Player:
    position: int
    score: int = 0

    @functools.cache
    def roll(self) -> dict[Player, int]:
        return {self.new_players_from_move(roll_result): count for roll_result, count in POSSIBLE_RESULTS.items()}

    @functools.cache
    def new_players_from_move(self, roll_result: int) -> Player:
        new_position = move(self.position, roll_result)
        return Player(
            position=new_position,
            score=self.score + new_position,
        )

    @property
    def has_won(self) -> bool:
        return self.score >= TARGET_SCORE


@dataclasses.dataclass(frozen=True)
class Game:
    player: Player
    opponent: Player

    def new_game_with_replaced(self, new_player: Player) -> Game:
        return Game(player=new_player, opponent=self.opponent)

    @functools.cache
    def roll(self) -> dict[Game, int]:
        games = {}
        new_players = self.player.roll()

        for player, count in new_players.items():
            games[self.new_game_with_replaced(player)] = count

        return games

    def mirror(self) -> Game:
        return Game(player=self.opponent, opponent=self.player)


def main(input_file: str = "input.txt") -> None:
    position_player_1, position_player_2 = parse_input(input_file)

    game = Game(player=Player(position=position_player_1), opponent=Player(position=position_player_2))

    wins = [0, 0]
    board: dict[Game, int] = defaultdict(int)
    board[game] = 1

    mirror = False
    while board:
        next_board: dict[Game, int] = defaultdict(int)
        wins[int(mirror)] += sum([board_iteration(game, count, next_board) for game, count in board.items()])
        board = {game.mirror(): count for game, count in next_board.items()}
        mirror = not mirror

    print(max(wins))


def board_iteration(game: Game, count: int, next_board: dict[Game, int]) -> int:
    total_wins = 0
    new_games = game.roll()
    for new_game, new_count in new_games.items():
        if new_game.player.has_won:
            total_wins += new_count * count
        else:
            next_board[new_game] += new_count * count
    return total_wins


def parse_input(input_file: str) -> list[int]:
    with open(input_file) as f:
        return list(f.read().splitlines() | select(lambda row: row.rsplit()[-1]) | select(int))


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
