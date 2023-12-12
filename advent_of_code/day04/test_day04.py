from pathlib import Path

import pytest

from advent_of_code.day04.scratchcards import Scratchcard, ScratchcardPile

## Puzzle tests


@pytest.mark.parametrize(
    "card_file,score",
    [
        ("advent_of_code/day04/input/sample", 13),
        ("advent_of_code/day04/input/puzzle", 20117),
    ],
)
def test_solves_day04_part1(card_file: str, score: int) -> None:
    pile = ScratchcardPile(Path(card_file))
    assert pile.score() == score


## Unit tests


def test_no_winning_numbers() -> None:
    card = Scratchcard("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
    assert card.score() == 0


def test_one_winning_number() -> None:
    card = Scratchcard("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
    assert card.score() == 1
