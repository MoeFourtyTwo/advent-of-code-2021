import fire


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        lines = f.read().splitlines()

    lines = [(left.split(" "), right.split(" ")) for left, right in [line.split(" | ") for line in lines]]

    count = 0
    for left, right in lines:
        for code in right:
            if len(code) in {2, 4, 3, 7}:
                count += 1

    print(count)


if __name__ == "__main__":
    fire.Fire(main)
