import re
from collections import Counter
from dataclasses import dataclass
from itertools import islice, tee
from pathlib import Path
from typing import Iterable


class Scratchcard:
    def __init__(self, text: str) -> None:
        self.id_text, numbers_text = text.split(":")
        self.your_text, self.winning_text = numbers_text.split("|")

    def points(self) -> int:
        your_winners_count = len(self.your_winners)
        if your_winners_count == 0:
            return 0
        # In theory `**` can return a float. https://github.com/python/mypy/issues/7765
        return 2 ** (your_winners_count - 1)  # type: ignore[no-any-return]

    @property
    def your_winners(self) -> set[int]:
        return self.to_set(self.your_text) & self.to_set(self.winning_text)

    def to_set(self, text: str) -> set[int]:
        return set(int(num.group(0)) for num in re.finditer(r"\d+", text))

    def __repr__(self) -> str:
        return self.id_text


def read_cards(card_file: Path) -> Iterable[Scratchcard]:
    with card_file.open() as f:
        for line in f:
            yield Scratchcard(line)


@dataclass
class PointsGame:
    card_file: Path

    def sum_points(self) -> int:
        return sum(card.points() for card in read_cards(self.card_file))


class CopiesGame:
    def __init__(self, card_file: Path) -> None:
        self.card_counter = Counter(read_cards(card_file))

    def count_originals_and_copies(self) -> int:
        card_iter = iter(self.card_counter)
        try:
            while True:
                card = next(card_iter)
                next_cards_to_copy = len(card.your_winners)
                number_of_copies = self.card_counter[card]
                card_iter, peeker = tee(card_iter)
                for next_card in islice(peeker, next_cards_to_copy):
                    self.card_counter[next_card] += number_of_copies
        except StopIteration:
            pass
        return self.card_counter.total()
