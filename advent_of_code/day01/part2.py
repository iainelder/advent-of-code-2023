#!/bin/env python3

import string
import sys
from pathlib import Path
from typing import Dict, Iterable

import regex


class Solution:
    def __init__(self, problem: Path, wordmap: Dict[str, int] = {}) -> None:
        self.problem = problem
        self.wordmap = wordmap or WORDMAP
        self.pattern = "|".join(self.wordmap)

    def calibration_sum(self) -> int:
        return sum(self.iter_calibration_values())

    def iter_calibration_values(self) -> Iterable[int]:
        with self.problem.open() as file:
            for line in file:
                yield self.get_calibration_value(line)

    def get_calibration_value(self, line: str) -> int:
        first = self.first_digit(line)
        last = self.first_digit(line, regex.REVERSE)
        return 10 * self.wordmap[first] + self.wordmap[last]

    def first_digit(self, line: str, flags: int = 0) -> str:
        match = regex.search(self.pattern, line, flags)
        if match:
            return match.group()
        raise ValueError(line)


WORDMAP = {
    **{d: int(d) for d in string.digits},
    **{
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    },
}


def main() -> None:
    problem = Path(sys.argv[1])
    print(Solution(problem, WORDMAP).calibration_sum())


if __name__ == "__main__":
    main()
