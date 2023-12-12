import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class Scratchcard:
    def __init__(self, text: str) -> None:
        self.your_text, self.winning_text = text.split(":")[1].split("|")

    def score(self) -> int:
        your_winners = self.to_set(self.your_text) & self.to_set(self.winning_text)
        if not your_winners:
            return 0
        # In theory `**` can return a float. https://github.com/python/mypy/issues/7765
        return 2 ** (len(your_winners) - 1)  # type: ignore[no-any-return]

    def to_set(self, text: str) -> set[int]:
        return set(int(num.group(0)) for num in re.finditer(r"\d+", text))


@dataclass
class ScratchcardPile:
    card_file: Path

    def score(self) -> int:
        return sum(card.score() for card in self.cards)

    @property
    def cards(self) -> Iterable[Scratchcard]:
        with self.card_file.open() as f:
            for line in f:
                yield Scratchcard(line)
