from pathlib import Path
import pytest
from advent_of_code.day05.almanac import Almanac
from advent_of_code.day05.seed_locator import SeedLocator


@pytest.mark.parametrize(
    "almanac_file,location_number",
    [
        (Path("advent_of_code/day05/input/sample"), 35),
        (Path("advent_of_code/day05/input/puzzle"), 650599855),
    ],
)
def test_solves_day05_part1(almanac_file: Path, location_number: int) -> None:
    almanac = Almanac.from_file(almanac_file)
    locator = SeedLocator.from_almanac(almanac)
    assert locator.lowest_location_number() == location_number


@pytest.mark.xfail(strict=True, reason="Not implemented")
@pytest.mark.parametrize(
    "almanac_file,location_number",
    [
        (Path("advent_of_code/day05/input/sample"), 46),
        # (Path("advent_of_code/day05/input/puzzle"), 0),
    ],
)
def test_solves_day05_part2(almanac_file: Path, location_number: int) -> None:
    # TODO: RangeLocator
    pytest.fail()
