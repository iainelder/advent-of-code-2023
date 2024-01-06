from itertools import islice
from typing import Iterable
from dataclasses import dataclass, field
from intervaltree import IntervalTree, Interval  # type: ignore[import-untyped]
from .almanac import Almanac, Map, MapRange


@dataclass(frozen=True)
class Number:
    category: str
    value: int
    locator: "SeedLocator" = field(repr=False)

    def __getitem__(self, item: str) -> "Number":
        *_, last = self.locator.iter_mappings(self, dest=item)
        return last


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
            number = self.number(
                category=map.dest, value=SeedLocator.map(tree, number.value)
            )
            yield number
