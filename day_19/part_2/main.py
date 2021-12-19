from __future__ import annotations

import dataclasses
import functools
import itertools
import timeit
from typing import Generator

import fire
import numpy as np
from pipe import select, where
from scipy.spatial.distance import cityblock
from scipy.spatial.transform import Rotation
from tqdm import tqdm, trange


def rotations() -> Generator[Rotation, None, None]:

    possible_rotations = [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
        [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
        [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
        [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
        [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
        [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
        [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
        [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
        [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
        [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
        [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
        [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
        [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
        [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
        [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
    ]
    for rotation in possible_rotations:
        yield Rotation.from_matrix(np.array(rotation))


@dataclasses.dataclass
class Map:
    name: str
    beacons: np.ndarray
    seen_offsets: list[np.ndarray] = dataclasses.field(default_factory=lambda: list([np.array([0, 0, 0])]))

    @classmethod
    def from_string(cls, rows: list[str], name: str) -> Map:
        return cls(
            beacons=np.array(list(rows | select(functools.partial(str.split, sep=","))), dtype=int),
            name=name.replace("---", "").strip().replace("scanner", "map"),
        )

    def try_merge(self, other_map: Map) -> bool:
        t = tqdm(rotations(), total=24, leave=False)
        t.set_description(f"Trying {self.name} with {other_map.name}")
        fixed_beacon_set = set(tuple(row) for row in self.beacons)
        for rotation in t:
            other_rotated = np.round(rotation.apply(other_map.beacons)).astype(int)
            for other_point in other_rotated:
                for fixed_point in fixed_beacon_set:
                    dist = -other_point + fixed_point
                    translated = other_rotated + dist

                    translated_set = set(tuple(row) for row in translated)

                    matches = translated_set & fixed_beacon_set

                    if len(matches) >= 12:
                        t.set_description(f"Trying {self.name} with {other_map.name}. Found a match at {dist}")
                        merged = np.array(list(translated_set | fixed_beacon_set))
                        other_map.beacons = merged
                        self.beacons = merged

                        rotated_offsets = np.round(rotation.apply(other_map.seen_offsets)).astype(int) + dist
                        self.seen_offsets.extend(rotated_offsets)

                        return True
        return False

    def __len__(self) -> int:
        return len(self.beacons)

    def __hash__(self):
        return hash(self.name)

    def __gt__(self, other):
        return len(self) > len(other)

    def __lt__(self, other):
        return len(self) < len(other)


def main(input_file: str = "input.txt") -> None:
    scanner_list = parse_input(input_file)

    final_map = merge_maps_pairwise(scanner_list)
    print(f"Beacon count: {len(final_map.beacons)}")

    max_dist = 0
    for left, right in itertools.combinations(final_map.seen_offsets, 2):
        dist = cityblock(left, right)
        max_dist = max(max_dist, dist)
    print(f"Max distance: {max_dist}")


def merge_maps_pairwise(scanner_list: list[Map]) -> Map:
    compared = set()

    for _ in trange(1, len(scanner_list)):
        combinations = sorted(itertools.combinations(scanner_list, 2))
        combinations = list(combinations | where(lambda v: frozenset(v) not in compared))
        for left, right in tqdm(combinations, leave=False):
            if left.try_merge(right):
                scanner_list.remove(right)
                compared = {comparison for comparison in compared if left not in comparison}
                break
            else:
                compared.add(frozenset([left, right]))
        else:
            raise Exception("Could not merge any maps")
    return scanner_list[0]


def parse_input(input_file: str) -> list[Map]:
    with open(input_file) as f:
        rows = f.read().splitlines()

    scanner_list = []
    current_scanner = []
    name_row = rows[0]
    for row in rows[1:]:
        if not row:
            continue
        if row.startswith("--- scanner "):
            scanner_list.append(Map.from_string(current_scanner, name_row))
            current_scanner = []
            name_row = row
        else:
            current_scanner.append(row)
    scanner_list.append(Map.from_string(current_scanner, name_row))
    return scanner_list


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
