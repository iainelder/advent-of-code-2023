from pathlib import Path
from typing import Iterable, List

import pytest
from lark import Token

from advent_of_code.day03.schematic import Schematic

# Puzzle tests


@pytest.mark.parametrize(
    "schematic_path,part_sum",
    [
        ("advent_of_code/day03/input/sample", 4361),
    ],
)
def test_solves_day03(schematic_path: str, part_sum: int) -> None:
    schematic = Schematic(Path(schematic_path))
    assert schematic.part_sum() == part_sum


# Unit tests


def write_lines(path: Path, lines: Iterable[str]) -> None:
    with path.open("w") as file:
        print(*lines, sep="\n", file=file)


@pytest.fixture()
def tmp_input(tmp_path: Path) -> Path:
    return tmp_path / "input"


@pytest.mark.parametrize(
    "lines,part_sum",
    [
        (["*"], 0),
        pytest.param(["1*"], 1),
    ],
)
def test_part_sum(tmp_input: Path, lines: str, part_sum: int) -> None:
    write_lines(tmp_input, lines)
    assert Schematic(tmp_input).part_sum() == part_sum


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            ["1"],
            [
                Token(
                    "INT",
                    "1",
                    start_pos=1,
                    line=1,
                    column=1,
                    end_line=1,
                    end_column=1,
                    end_pos=1,
                )
            ],
        )
    ],
)
def test_iter_tokens(tmp_input: Path, lines: str, expected: List[str]) -> None:
    write_lines(tmp_input, lines)
    assert expected == list(Schematic(tmp_input).iter_tokens())
