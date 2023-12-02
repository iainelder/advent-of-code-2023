from pathlib import Path

import pytest

from advent_of_code.day02.part1 import Bag, Solution


@pytest.mark.xfail(strict=True, reason="Not implemented")
def test_day02_part1() -> None:
    solution = Solution(
        game_list=Path("tests/day02/small_input"),
        bag=Bag(red=12, green=13, blue=14),
    )
    assert solution.possible_game_sum() == 8
