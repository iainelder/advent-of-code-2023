from pytest import CaptureFixture
from pathlib import Path
import sys
from unittest.mock import patch
from advent_of_code.day01.part1 import main
from advent_of_code.day01.part2 import Solution, WORDMAP


def test_day01_part1(capsys: CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["test_part1", "tests/day01/input"]):
        main()
    out, err = capsys.readouterr()
    assert out == "55447\n"


def test_day01_part2() -> None:
    assert Solution(Path("tests/day01/input"), WORDMAP).calibration_sum() == 54706
