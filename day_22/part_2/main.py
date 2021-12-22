from __future__ import annotations

import dataclasses
import timeit
from typing import Optional

import fire
from pipe import select
from tqdm import tqdm


@dataclasses.dataclass(order=True)
class Span:
    v_min: int
    v_max: int

    @classmethod
    def from_inclusive(cls, v_min: int, v_max: int) -> Span:
        return cls(v_min=v_min, v_max=v_max + 1)

    def intersect(self, other: Span) -> Optional[list[Span]]:
        if self.v_max <= other.v_min or other.v_max <= self.v_min:
            return

        total_min = min(self.v_min, other.v_min)
        first_intersect = max(self.v_min, other.v_min)
        second_intersect = min(self.v_max, other.v_max)
        total_max = max(self.v_max, other.v_max)

        spans = [
            Span(total_min, first_intersect),
            Span(first_intersect, second_intersect),
            Span(second_intersect, total_max),
        ]
        return [span for span in spans if span.valid]

    @property
    def valid(self) -> bool:
        return self.v_min < self.v_max

    def __len__(self):
        return self.v_max - self.v_min

    def __contains__(self, item: Span) -> bool:
        return item.v_min >= self.v_min and item.v_max <= self.v_max


@dataclasses.dataclass
class Cuboid:
    x: Span
    y: Span
    z: Span
    value: bool

    def intersect(self, other: Cuboid) -> list[Cuboid]:
        intersect_x = self.x.intersect(other.x)
        intersect_y = self.y.intersect(other.y)
        intersect_z = self.z.intersect(other.z)

        if intersect_x is None or intersect_y is None or intersect_z is None:
            return [self]

        if self in other and other.value:
            return []

        cuboids = []
        for x in intersect_x:
            for y in intersect_y:
                for z in intersect_z:
                    cuboid = Cuboid(x, y, z, self.value)
                    if cuboid in self and cuboid not in other:
                        cuboids.append(cuboid)

        return cuboids

    @property
    def volume(self) -> int:
        return len(self.x) * len(self.y) * len(self.z)

    def __contains__(self, item: Cuboid) -> bool:
        return item.x in self.x and item.y in self.y and item.z in self.z


def main(input_file: str = "input.txt") -> None:
    cuboids = parse_input(input_file)

    cuboid, *remaining_cuboids = cuboids
    cuboids = [cuboid]

    t = tqdm(remaining_cuboids)
    t.set_description(f"{len(cuboids)} Cuboids")
    for new_cuboid in t:
        intersected_cuboids = []
        for previous_cuboid in cuboids:
            intersected_cuboids += previous_cuboid.intersect(new_cuboid)
        if new_cuboid.value:
            intersected_cuboids.append(new_cuboid)

        cuboids = intersected_cuboids
        t.set_description(f"{len(cuboids)} Cuboids")
        pass

    print(sum(cuboid.volume for cuboid in cuboids))


def parse_input(input_file: str) -> list[Cuboid]:
    with open(input_file) as f:
        return list(f.read().splitlines() | select(parse_line))


def parse_line(line: str) -> Cuboid:
    on = int(line.startswith("on "))
    line = (
        line.replace("on ", "")
        .replace("off ", "")
        .replace("x=", "")
        .replace("y=", "")
        .replace("z=", "")
        .replace("..", ",")
    )
    x_min, x_max, y_min, y_max, z_min, z_max = map(int, line.split(","))

    return Cuboid(
        Span.from_inclusive(x_min, x_max),
        Span.from_inclusive(y_min, y_max),
        Span.from_inclusive(z_min, z_max),
        bool(on),
    )


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
