import dataclasses

import fire
import numpy as np


@dataclasses.dataclass
class Board:
    values: np.ndarray
    crossed_out: np.ndarray = dataclasses.field(default_factory=lambda: np.zeros(shape=(5, 5), dtype=bool))

    def has_won(self) -> bool:
        for i in range(5):
            if all(self.crossed_out[i, :]) or all(self.crossed_out[:, i]):
                return True
        return False

    def hit(self, value: int) -> None:
        for i in range(5):
            for j in range(5):
                if self.values[i, j] == value:
                    self.crossed_out[i, j] = True

    def score(self) -> int:
        return int(np.sum(self.values[~self.crossed_out], axis=None))


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        draws = list(map(int, f.readline().split(",")))
        lines = [np.array(line.split()).astype(int) for line in f.readlines() if line.strip()]

        boards = []

        while lines:
            current, lines = lines[:5], lines[5:]
            boards.append(Board(values=np.array(current)))

    for draw in draws:
        for board in boards:
            board.hit(draw)
            if board.has_won():
                print(board.score() * draw)
                return


if __name__ == "__main__":
    fire.Fire(main)
