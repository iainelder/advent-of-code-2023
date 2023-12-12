from pathlib import Path
from typing import Iterable

import pytest

from advent_of_code.day04.scratchcards import CopiesGame, PointsGame, Scratchcard

## Puzzle tests


@pytest.mark.parametrize(
    "card_file,score",
    [
        ("advent_of_code/day04/input/sample", 13),
        ("advent_of_code/day04/input/puzzle", 20117),
    ],
)
def test_solves_day04_part1(card_file: str, score: int) -> None:
    game = PointsGame(Path(card_file))
    assert game.sum_points() == score


@pytest.mark.parametrize(
    "card_file,score",
    [
        ("advent_of_code/day04/input/sample", 30),
    ],
)
def test_solves_day04_part2(card_file: str, score: int) -> None:
    game = CopiesGame(Path(card_file))
    assert game.count_originals_and_copies() == score


## Unit tests


def write_lines(path: Path, lines: Iterable[str]) -> None:
    with path.open("w") as file:
        print(*lines, sep="\n", file=file)


@pytest.fixture()
def tmp_input(tmp_path: Path) -> Path:
    return tmp_path / "input"


def test_no_winning_numbers() -> None:
    card = Scratchcard("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
    assert card.points() == 0


def test_one_winning_number() -> None:
    card = Scratchcard("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
    assert card.points() == 1


def test_four_winning_numbers() -> None:
    card = Scratchcard("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert card.points() == 8


@pytest.mark.parametrize(
    "lines,expected",
    [
        (["Card 1: 1 | 1", "Card 2: 0 | 1"], 3),
        (["Card 1: 1 2 | 1 2", "Card 2: 0 | 1"], 4),
    ],
)
def test_small_copy_game(tmp_input: Path, lines: list[str], expected: int) -> None:
    write_lines(tmp_input, lines)
    CopiesGame(tmp_input).count_originals_and_copies() == expected
