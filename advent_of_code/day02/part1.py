from functools import reduce
from math import prod
from operator import or_
from pathlib import Path
from typing import Counter, Iterable, Tuple


class Game:
    def __init__(self, line: str) -> None:
        self._gameline, self._handsline = line.split(":")

    @property
    def id(self) -> int:
        return int(self._gameline.strip("Game "))

    @property
    def hands(self) -> Iterable[Counter[str]]:
        for handline in self._handsline.split(";"):
            yield Game._build_hand(handline)

    @staticmethod
    def _build_hand(handline: str) -> Counter[str]:
        return Counter(dict(Game._hand_tuples(handline)))

    @staticmethod
    def _hand_tuples(handline: str) -> Iterable[Tuple[str, int]]:
        for part in handline.split(","):
            count, color = part.strip().split(" ")
            yield (color, int(count))

    def possible_in_bag(self, bag: Counter[str]) -> bool:
        return self.max_hand() <= bag

    def max_hand(self) -> Counter[str]:
        return reduce(or_, self.hands)

    def power(self) -> int:
        return prod(self.max_hand().values())


class Solution:
    def __init__(self, *, game_list: Path, bag: Counter[str]) -> None:
        self.game_list = game_list
        self.bag = bag

    def possible_game_id_sum(self) -> int:
        return sum(game.id for game in self.possible_games())

    def power_sum(self) -> int:
        return sum(game.power() for game in self.games())

    def possible_games(self) -> Iterable[Game]:
        for game in self.games():
            if game.possible_in_bag(self.bag):
                yield game

    def games(self) -> Iterable[Game]:
        with self.game_list.open() as file:
            for line in file:
                yield Game(line)
