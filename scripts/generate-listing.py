from pathlib import Path
from argparse import ArgumentParser
import json


def main():
    parser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    listing = [
        p.relative_to(input_path).as_posix()
        for p in input_path.glob("**/*")
        if not p.is_dir()
    ]
    output_path.write_text(json.dumps(listing, indent=2))


if __name__ == "__main__":
    main()
