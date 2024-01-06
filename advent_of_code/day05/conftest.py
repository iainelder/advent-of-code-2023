import pytest
from pathlib import Path
from advent_of_code.day05.almanac import Almanac
from advent_of_code.day05.seed_locator import SeedLocator
from advent_of_code.day05.range_locator import RangeLocator


@pytest.fixture
def almanac() -> Almanac:
    return Almanac.from_file(Path("advent_of_code/day05/input/sample"))


@pytest.fixture
def seed_locator(almanac: Almanac) -> SeedLocator:
    return SeedLocator.from_almanac(almanac)


@pytest.fixture
def range_locator(almanac: Almanac) -> RangeLocator:
    return RangeLocator.from_almanac(almanac)
