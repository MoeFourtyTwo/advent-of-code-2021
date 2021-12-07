import fire


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        data = [x.split() for x in f.read().splitlines()]

    horizontal_pos = 0
    depth = 0
    aim = 0

    for command, value in data:
        value = int(value)
        if command == "up":
            aim -= value
        elif command == "down":
            aim += value
        elif command == "forward":
            horizontal_pos += value
            depth += aim * value
        else:
            raise ValueError(f"Unexpected command {command}")

    print(horizontal_pos * depth)


if __name__ == "__main__":
    fire.Fire(main)
