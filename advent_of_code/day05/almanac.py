from itertools import islice
from typing import cast, Sequence, Iterable
from lark import Lark, Transformer, Token
from dataclasses import dataclass, field
from pathlib import Path
from intervaltree import IntervalTree, Interval  # type: ignore[import-untyped]


@dataclass(frozen=True)
class MapRange:
    dest_start: int
    source_start: int
    source_length: int

    def interval(self) -> Interval:
        return Interval(
            begin=self.source_start,
            end=self.source_start + self.source_length,
            data=self.dest_start,
        )


@dataclass(frozen=True)
class Map:
    source: str
    dest: str
    ranges: Sequence[MapRange]
    tree: IntervalTree = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "tree", IntervalTree(r.interval() for r in self.ranges)
        )

    def map(self, value: int) -> int:
        for iv in self.tree[value]:
            offset: int = iv.data - iv.begin
            return value + offset
        return value


@dataclass(frozen=True)
class Number:
    category: str
    value: int
    locator: "SeedLocator" = field(repr=False)

    def __getitem__(self, item: str) -> "Number":
        *_, last = self.locator.iter_mappings(self, dest=item)
        return last


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


@dataclass(frozen=True)
class SeedLocator:
    almanac: Almanac
    intervals: list[IntervalTree]

    @staticmethod
    def from_almanac(almanac: Almanac) -> "SeedLocator":
        intervals = [SeedLocator.tree(m) for m in almanac.maps]
        return SeedLocator(almanac, intervals)

    @staticmethod
    def interval(mr: MapRange) -> Interval:
        return Interval(
            begin=mr.source_start,
            end=mr.source_start + mr.source_length,
            data=mr.dest_start,
        )

    @staticmethod
    def tree(m: Map) -> IntervalTree:
        return IntervalTree(SeedLocator.interval(r) for r in m.ranges)

    def seed(self, value: int) -> Number:
        return self.number("seed", value)

    def number(self, category: str, value: int) -> Number:
        return Number(category=category, value=value, locator=self)

    def lowest_location_number(self) -> int:
        return min(self.seed(n)["location"].value for n in self.almanac.seed_numbers)

    @staticmethod
    def map(tree: IntervalTree, value: int) -> int:
        for iv in tree[value]:
            offset: int = iv.data - iv.begin
            return value + offset
        return value

    def iter_mappings(
        self, number: Number, dest: str | None = None
    ) -> Iterable[Number]:
        yield number

        if number.category == dest:
            return

        start = self.almanac.categories.index(number.category)

        if dest is None:
            stop = len(self.almanac.categories)
        else:
            stop = self.almanac.categories.index(dest)

        if stop < start:
            raise ValueError(f"'{dest}' precedes in list")

        for tree, map in islice(zip(self.intervals, self.almanac.maps), start, stop):
            number = self.number(category=map.dest, value=self.map(tree, number.value))
            yield number
