from collections import Counter
from pathlib import Path

import pytest

from advent_of_code.day02.part1 import Game, Solution

# Puzzle tests


def test_day02_part1() -> None:
    solution = Solution(
        game_list=Path("tests/day02/small_input"),
        bag=Counter(red=12, green=13, blue=14),
    )
    assert solution.possible_game_id_sum() == 8


# Unit tests


@pytest.fixture()
def game1() -> Game:
    return Game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")


def test_game_has_id(game1: Game) -> None:
    assert game1.id == 1


def test_game_has_hands(game1: Game) -> None:
    assert list(game1.hands) == [
        Counter(blue=3, red=4),
        Counter(red=1, green=2, blue=6),
        Counter(green=2),
    ]


def test_game_has_max_hand(game1: Game) -> None:
    assert game1.max_hand() == Counter(blue=6, red=4, green=2)


def test_bag_includes_possible_game(game1: Game) -> None:
    bag = Counter(blue=6, red=4, green=2)
    assert game1.possible_in_bag(bag)


def test_bag_doesnt_include_impossible_game(game1: Game) -> None:
    bag = Counter(red=1, green=1, blue=1)
    assert not game1.possible_in_bag(bag)
