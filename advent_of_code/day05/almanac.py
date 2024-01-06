from typing import cast, Sequence
from lark import Lark, Transformer, Token
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MapRange:
    dest_start: int
    source_start: int
    source_length: int


@dataclass(frozen=True)
class Map:
    source: str
    dest: str
    ranges: Sequence[MapRange]


@dataclass(frozen=True)
class Almanac:
    seed_numbers: Sequence[int]
    maps: Sequence[Map]
    categories: list[str] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "categories", [m.source for m in self.maps] + [self.maps[-1].dest]
        )

    @classmethod
    def from_file(cls, almanac_file: Path) -> "Almanac":
        tree = Lark(GRAMMAR, start="almanac").parse(almanac_file.read_text())
        return cast("Almanac", AlmanacTransformer().transform(tree))


# Lark doesn't document any type args.
class AlmanacTransformer(Transformer):  # type: ignore[type-arg]
    def almanac(self, items: list[list[int] | Map]) -> Almanac:
        return Almanac(
            seed_numbers=cast(list[int], items[0]), maps=cast(list[Map], items[1:])
        )

    def seeds(self, items: list[Token]) -> list[int]:
        return [int(i) for i in items]

    def map(self, items: list[Token | MapRange]) -> Map:
        return Map(
            source=str(items[0]),
            dest=str(items[1]),
            ranges=cast(list[MapRange], items[2:]),
        )

    def range(self, items: list[Token]) -> MapRange:
        return MapRange(
            dest_start=int(items[0]),
            source_start=int(items[1]),
            source_length=int(items[2]),
        )


GRAMMAR = r"""
almanac: seeds map+
seeds: "seeds:" INT+
map: WORD "-to-" WORD " map:" range+
range: INT INT INT

%import common.WORD
%import common.INT
%import common.WS
%ignore WS
"""
