import fire


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        data = [int(x) for x in f.read().splitlines()]

    count = sum(cur > prev for prev, cur in zip(data[:-1], data[1:]))

    print(count)


if __name__ == "__main__":
    fire.Fire(main)
