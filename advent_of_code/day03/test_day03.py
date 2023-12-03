from pathlib import Path
from typing import Iterable

import pytest
from lark import Lark

from advent_of_code.day03.schematic import Schematic


def write_lines(path: Path, lines: Iterable[str]):
    with path.open("w") as file:
        print(*lines, file=file)


@pytest.fixture()
def tmp_input(tmp_path: Path) -> Path:
    return tmp_path / "input"


@pytest.mark.parametrize(
    "lines,part_sum",
    [
        (["*"], 0),
        (["1*"], 1),
    ],
)
def test_part_sum(tmp_input: Path, lines: str, part_sum: int):
    write_lines(tmp_input, lines)
    assert Schematic(tmp_input).part_sum() == part_sum


@pytest.mark.parametrize(
    "lines",
    [
        ("1 22 333",),
    ],
)
def test_lark(tmp_input: Path, lines: str):
    write_lines(tmp_input, lines)

    grammar = r"""
    start: NUMBER*
    %import common.NUMBER
    %import common.WS
    %ignore WS
    """

    parser = Lark(grammar)

    with tmp_input.open() as file:
        values = list(token.value for token in parser.lex(file.read()))
        assert values == ["1", "22", "333"]
