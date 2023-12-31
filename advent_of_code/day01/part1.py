#!/bin/env python3

import string
import sys
from pathlib import Path
from typing import Iterable, Set


def main() -> None:
    problem = Path(sys.argv[1])
    calibration_sum = sum(iter_calibration_values(problem))
    print(calibration_sum)


def iter_calibration_values(problem: Path) -> Iterable[int]:
    with problem.open() as file:
        for line in file:
            if line == "\n":
                continue
            yield get_calibration_value(line)


def get_calibration_value(line: str) -> int:
    first = first_digit(line)
    last = first_digit(reversed(line))
    return 10 * int(first) + int(last)


def first_digit(line: Iterable[str], digits: Set[str] = set(string.digits)) -> str:
    for char in line:
        if char in digits:
            return char
    raise ValueError(line)


if __name__ == "__main__":
    main()
