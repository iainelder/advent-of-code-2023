from pathlib import Path
from typing import NamedTuple


class Bag(NamedTuple):
    red: int
    green: int
    blue: int


class Solution:
    def __init__(self, *, game_list: Path, bag: Bag) -> None:
        self.game_list = game_list
        self.bag = bag

    def possible_game_sum(self) -> int:
        return 0
