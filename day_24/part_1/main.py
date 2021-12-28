from __future__ import annotations

import timeit

import fire
import pandas as pd
from tqdm import tqdm


def main(input_file: str = "input.txt", search_max: bool = True) -> None:
    instructions = parse_instructions(input_file)
    alus = pd.DataFrame(
        {
            "w": [0],
            "x": 0,
            "y": 0,
            "z": 0,
            "input": 0,
        }
    )
    t = tqdm(instructions)
    for instruction in t:
        t.set_description(f"Working with {len(alus)} ALUs")
        if len(instruction) == 3:
            instruction, arg_a, arg_b = instruction
            if instruction == "add":
                alus[arg_a] += alus[arg_b]
            elif instruction == "mul":
                alus[arg_a] *= alus[arg_b]
            elif instruction == "mod":
                alus[arg_a] %= alus[arg_b]
                alus = optimize(alus, t)
            elif instruction == "div":
                alus[arg_a] = (alus[arg_a] / alus[arg_b]).astype(int)
                alus = optimize(alus, t)
            elif instruction == "eql":
                alus[arg_a] = (alus[arg_a] == alus[arg_b]).astype(int)
                alus = optimize(alus, t)
            elif instruction == "add_value":
                alus[arg_a] += arg_b
            elif instruction == "mul_value":
                alus[arg_a] *= arg_b
            elif instruction == "mod_value":
                alus[arg_a] %= arg_b
                alus = optimize(alus, t)
            elif instruction == "div_value":
                alus[arg_a] = (alus[arg_a] / arg_b).astype(int)
                alus = optimize(alus, t)
            elif instruction == "eql_value":
                alus[arg_a] = (alus[arg_a] == arg_b).astype(int)
                alus = optimize(alus, t)
        else:
            alus = optimize(alus, t)
            t.set_description(f"New input data. Increasing number of ALUs to {9 * len(alus)}")
            alus["input"] *= 10
            target_df = pd.DataFrame(columns=alus.columns)
            for i in range(9, 0, -1) if search_max else range(1, 10):
                new_df = alus.copy()
                new_df["input"] += i
                new_df[instruction[1]] = i
                target_df = target_df.append(new_df)
            alus = target_df
            alus = optimize(alus, t)

    valid_rows = alus[alus["z"] == 0]
    print(f"Value: {valid_rows['input'].max() if search_max else valid_rows['input'].min()}")


def optimize(alus: pd.DataFrame, t) -> pd.DataFrame:
    t.set_description(f"Optimizing {len(alus)} ALUs")
    alus.drop_duplicates(subset=["w", "x", "y", "z"], inplace=True)
    t.set_description(f"Working with {len(alus)} ALUs")
    return alus


def parse_instructions(input_file: str) -> list[tuple[str, str] | tuple[str, str, str | int]]:
    with open(input_file) as f:
        lines = f.read().splitlines()
    instructions = []
    for line in lines:
        instruction, *args = line.split()

        if len(args) == 2:
            arg_a, arg_b = args
            if arg_b in "wxzy":
                instructions.append((instruction, arg_a, arg_b))
            else:
                instructions.append((instruction + "_value", arg_a, int(arg_b)))
        else:
            instructions.append((instruction, args[0]))
    return instructions


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
