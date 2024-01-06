from dataclasses import dataclass, field
from .almanac import Almanac


@dataclass(frozen=True)
class NumberRange:
    category: str
    start: int
    end: int
    locator: "RangeLocator" = field(repr=False)

    def break_down(self) -> list["NumberRange"]:
        return [self]


@dataclass(frozen=True)
class RangeLocator:
    almanac: Almanac

    @staticmethod
    def from_almanac(almanac: Almanac) -> "RangeLocator":
        return RangeLocator(almanac)

    def seed(self, start: int, end: int) -> NumberRange:
        return self.number_range(category="seed", start=start, end=end)

    def number_range(self, category: str, start: int, end: int) -> NumberRange:
        return NumberRange(category=category, start=start, end=end, locator=self)
