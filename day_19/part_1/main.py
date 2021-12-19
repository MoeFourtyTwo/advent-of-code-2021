from __future__ import annotations

import dataclasses
import functools
import itertools
import timeit
from typing import Generator

import fire
import numpy as np
from pipe import select, where
from scipy.spatial.transform import Rotation
from tqdm import tqdm


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

    @classmethod
    def from_string(cls, rows: list[str], name: str) -> Map:
        return cls(
            beacons=np.array(list(rows | select(functools.partial(str.split, sep=","))), dtype=int),
            name=name.replace("---", "").strip(),
        )

    def try_merge(self, fixed_map: Map) -> bool:
        t = tqdm(rotations(), total=24)
        t.set_description(f"Trying {self.name} with {fixed_map.name}")
        fixed_beacon_set = set(tuple(row) for row in fixed_map.beacons)
        for rotation in t:
            rotated = np.round(rotation.apply(self.beacons)).astype(int)
            for point in rotated:
                for fixed_point in fixed_beacon_set:
                    translated = rotated + -point + fixed_point

                    translated_set = set(tuple(row) for row in translated)

                    matches = translated_set & fixed_beacon_set

                    if len(matches) >= 12:
                        t.set_description(
                            f"Trying {self.name} with {fixed_map.name}. Found a match at {-point + fixed_point}"
                        )
                        merged = np.array(list(translated_set | fixed_beacon_set))
                        fixed_map.beacons = merged
                        self.beacons = merged

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


def display_sorted(arr):
    for row in sorted(tuple(row) for row in arr):
        print(row)


def main(input_file: str = "input.txt") -> None:
    scanner_list = parse_input(input_file)

    final_map = merge_maps_pairwise(scanner_list)
    print(f"Beacon count: {len(final_map.beacons)}")


def merge_maps_pairwise(scanner_list: list[Map]) -> Map:
    compared = set()

    while len(scanner_list) > 1:
        combinations = sorted(itertools.combinations(scanner_list, 2))
        combinations = list(combinations | where(lambda v: frozenset(v) not in compared))
        for left, right in combinations:
            if left.try_merge(right):
                scanner_list.remove(right)
                compared = {comparison for comparison in compared if left not in comparison}
                print(f"\nRemaining: {len(scanner_list)}")
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
