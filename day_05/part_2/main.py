import dataclasses

import fire
import numpy as np

import matplotlib.pyplot as plt


@dataclasses.dataclass
class Point:
    x: int
    y: int


@dataclasses.dataclass
class Line:
    point_1: Point
    point_2: Point

    @staticmethod
    def parse_row(line: str) -> "Line":
        point_1, point_2 = [
            tuple(map(int, point.split(","))) for point in line.split(" -> ")
        ]
        return Line(
            point_1=Point(*point_1),
            point_2=Point(*point_2),
        )

    def is_horizontal_or_vertical(self) -> bool:
        return self.point_1.x == self.point_2.x or self.point_1.y == self.point_2.y

    def is_45_degrees(self) -> bool:
        return self.point_1.x - self.point_2.x == self.point_1.y - self.point_2.y

    def is_135_degrees(self) -> bool:
        return self.point_1.x - self.point_2.x == -(self.point_1.y - self.point_2.y)

    def draw(self, canvas: np.ndarray) -> None:
        x_min, x_max = min(self.point_1.x, self.point_2.x), max(
            self.point_1.x, self.point_2.x
        )
        y_min, y_max = min(self.point_1.y, self.point_2.y), max(
            self.point_1.y, self.point_2.y
        )
        if self.is_horizontal_or_vertical():
            canvas[x_min : x_max + 1, y_min : y_max + 1] += 1
        elif self.is_45_degrees():
            for i in range(x_max - x_min + 1):
                canvas[x_min + i, y_min + i] += 1
        elif self.is_135_degrees():
            for i in range(x_max - x_min + 1):
                canvas[x_max - i, y_min + i] += 1
        else:
            raise NotImplementedError

    def max_x(self) -> int:
        return max(self.point_1.x, self.point_2.x)

    def max_y(self) -> int:
        return max(self.point_1.y, self.point_2.y)


def main(plot: bool = False, input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = list(map(Line.parse_row, f.readlines()))

    lines = [
        line
        for line in lines
        if line.is_horizontal_or_vertical()
        or line.is_45_degrees()
        or line.is_135_degrees()
    ]

    dim_x = max(line.max_x() for line in lines)
    dim_y = max(line.max_y() for line in lines)

    canvas = np.zeros(shape=(dim_x, dim_y))

    for line in lines:
        line.draw(canvas)

    if plot:
        plt.imshow(canvas)
        plt.show()

    intersection_count = len(np.where(canvas > 1)[0])

    print(intersection_count)


if __name__ == "__main__":
    fire.Fire(main)
