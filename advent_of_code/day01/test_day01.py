import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from pytest import CaptureFixture

from advent_of_code.day01 import part1, part2


@pytest.mark.parametrize(
    "document,value",
    [
        ("advent_of_code/day01/input/part1_sample", "142\n"),
        ("advent_of_code/day01/input/puzzle", "55447\n"),
    ],
)
def test_solve_part1(capsys: CaptureFixture[str], document: str, value: str) -> None:
    with patch.object(sys, "argv", ["test_part1", document]):
        part1.main()
    out, _ = capsys.readouterr()
    assert out == value


@pytest.mark.parametrize(
    "document,value",
    [
        ("advent_of_code/day01/input/part2_sample", 281),
        ("advent_of_code/day01/input/puzzle", 54706),
    ],
)
def test_solve_part2(document: str, value: int) -> None:
    assert part2.Solution(Path(document)).calibration_sum() == value
