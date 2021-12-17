from __future__ import annotations

import dataclasses
import itertools
import timeit

import fire
from pipe import select


@dataclasses.dataclass
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def missed(self, area: Area) -> bool:
        return self.x > area.top_right.x or self.y < area.bottom_left.y

    def decay_velocity(self) -> None:
        if self.x > 0:
            self.x -= 1
        if self.x < 0:
            self.x += 1
        self.y -= 1


@dataclasses.dataclass
class Area:
    bottom_left: Vector
    top_right: Vector

    def __contains__(self, position: Vector) -> bool:
        return (
            self.bottom_left.x <= position.x <= self.top_right.x
            and self.bottom_left.y <= position.y <= self.top_right.y
        )


@dataclasses.dataclass
class Trajectory:
    positions: list[Vector] = dataclasses.field(default_factory=list)

    def max_y(self) -> int:
        return max(self.positions, key=lambda p: p.y).y

    def __add__(self, position: Vector) -> Trajectory:
        self.positions.append(position)
        return self


def next_step(position: Vector, velocity: Vector) -> tuple[Vector, Vector]:
    position += velocity
    velocity.decay_velocity()
    return position, velocity


def generate_trajectory(initial_velocity: Vector, target_area: Area) -> tuple[bool, Trajectory]:
    position = Vector(0, 0)

    trajectory = Trajectory()
    while True:
        position, velocity = next_step(position, initial_velocity)
        trajectory += position

        if position in target_area:
            return True, trajectory

        if position.missed(target_area):
            return False, trajectory


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        # noinspection PyUnresolvedReferences
        x_min, x_max, y_min, y_max = f.read().strip().replace("target area: x=", "").replace(", y=", "..").split(
            ".."
        ) | select(int)

    area = Area(Vector(x_min, y_min), Vector(x_max, y_max))

    max_y = 0
    for x, y in itertools.product(range(1, x_max + 1), range(y_min, 2 * abs(y_max))):
        initial_velocity = Vector(x, y)
        success, trajectory = generate_trajectory(initial_velocity, area)
        if success:
            max_y = max(max_y, trajectory.max_y())

    print(max_y)


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
