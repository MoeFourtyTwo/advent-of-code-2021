from __future__ import annotations

import dataclasses
import functools
import json
import math
import operator
import timeit
from typing import Union, Optional, Generator

import fire
from pipe import select


@dataclasses.dataclass
class SnailFishPairLeaf:
    value: int
    parent: SnailFishPair = None

    def __add__(self, other: Union[int, SnailFishPairLeaf]) -> SnailFishPairLeaf:
        if isinstance(other, int):
            self.value += other
            return self
        if isinstance(other, SnailFishPairLeaf):
            self.value += other.value
            return self

    @property
    def depth(self) -> int:
        count = 0
        node = self
        while node.parent is not None:
            count += 1
            node = node.parent
        return count

    @property
    def max(self) -> int:
        return self.value

    @property
    def magnitude(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f"{self.value}"

    def __len__(self) -> int:
        return 1

    def __getitem__(self, index: int) -> SnailFishPairLeaf:
        assert index == 0, f"Was asked for index {index} but only 0 is supported"
        return self

    def __setitem__(self, index: int, value: int) -> None:
        assert index == 0, f"Was asked for index {index} but only 0 is supported"
        self.value = value

    def __iter__(self) -> SnailFishPairLeaf:
        yield self


@dataclasses.dataclass
class SnailFishPair:
    left: Union[SnailFishPairLeaf, SnailFishPair]
    right: Union[SnailFishPairLeaf, SnailFishPair]
    parent: Optional[SnailFishPair] = None

    def __post_init__(self):
        if self.left.parent is None:
            self.left.parent = self
        if self.right.parent is None:
            self.right.parent = self

    def __add__(self, other: SnailFishPair) -> SnailFishPair:
        return SnailFishPair(left=self, right=other).reduce()

    def reduce(self) -> SnailFishPair:
        if self.depth > 4:
            return self.explode().reduce()
        if self.max >= 10:
            return self.split().reduce()
        return self

    @property
    def depth(self) -> int:
        return max(self.left.depth, self.right.depth)

    @property
    def max(self) -> int:
        return max(self.left.max, self.right.max)

    @property
    def magnitude(self) -> int:
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def explode(self) -> SnailFishPair:
        assert self.depth > 4
        for index, node in enumerate(self):
            if node.depth > 4:
                add_left, add_right = node.value, self[index + 1].value

                if node.parent.parent.left is node.parent:
                    node.parent.parent.left = SnailFishPairLeaf(value=0, parent=node.parent.parent)
                else:
                    node.parent.parent.right = SnailFishPairLeaf(value=0, parent=node.parent.parent)
                if index > 0:
                    self[index - 1] + add_left
                if index < len(self) - 1:
                    self[index + 1] + add_right
                return self

    def split(self) -> SnailFishPair:
        assert self.max >= 10
        for node in self:
            if node.value >= 10:
                new_pair = SnailFishPair.parse([math.floor(node.value / 2), math.ceil(node.value / 2)])

                if node.parent.left is node:
                    node.parent.left = new_pair
                    new_pair.parent = node.parent
                else:
                    node.parent.right = new_pair
                    new_pair.parent = node.parent

                return self

    def __len__(self):
        return len(self.left) + len(self.right)

    def __str__(self) -> str:
        return f"[{self.left}, {self.right}]"

    def __getitem__(self, index: int) -> SnailFishPairLeaf:
        if index < len(self.left):
            return self.left[index]
        else:
            return self.right[index - len(self.left)]

    def __setitem__(self, index: int, value: int) -> None:
        if index < len(self.left):
            self.left[index] = value
        else:
            self.right[index - len(self.left)] = value

    def __iter__(self) -> Generator[SnailFishPairLeaf, None, None]:
        yield from self.left
        yield from self.right

    @classmethod
    def parse(cls, data: list, parent: Optional[SnailFishPair] = None) -> SnailFishPair:
        assert isinstance(data, list) and len(data) == 2
        left, right = data
        if isinstance(left, int):
            left = SnailFishPairLeaf(value=left)
        else:
            left = SnailFishPair.parse(left)
        if isinstance(right, int):
            right = SnailFishPairLeaf(value=right)
        else:
            right = SnailFishPair.parse(right)
        return cls(left=left, right=right, parent=parent)


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        snail_fish_numbers = list(f.read().splitlines() | select(json.loads)) | select(SnailFishPair.parse)

    number = functools.reduce(operator.add, snail_fish_numbers)
    print(number.magnitude)


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
