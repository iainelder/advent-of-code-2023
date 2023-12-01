import sys
from pathlib import Path
from unittest.mock import patch

from pytest import CaptureFixture

import advent_of_code.day01.part1
import advent_of_code.day01.part2


def test_day01_part1(capsys: CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["test_part1", "tests/day01/input"]):
        advent_of_code.day01.part1.main()
    out, err = capsys.readouterr()
    assert out == "55447\n"


def test_day01_part2() -> None:
    solution = advent_of_code.day01.part2.Solution(Path("tests/day01/input"))
    assert solution.calibration_sum() == 54706
