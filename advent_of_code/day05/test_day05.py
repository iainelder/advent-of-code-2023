from pathlib import Path
import pytest
from advent_of_code.day05.almanac import Almanac, SeedLocator


# Puzzle tests


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


# Unit tests


@pytest.fixture
def almanac() -> Almanac:
    return Almanac.from_file(Path("advent_of_code/day05/input/sample"))


def test_almanac_has_seed_numbers(almanac: Almanac) -> None:
    assert almanac.seed_numbers == [79, 14, 55, 13]


def test_almanac_has_categories(almanac: Almanac) -> None:
    assert almanac.categories == [
        "seed",
        "soil",
        "fertilizer",
        "water",
        "light",
        "temperature",
        "humidity",
        "location",
    ]


# TODO: Test almanac has maps, ranges


@pytest.fixture
def seed_locator(almanac: Almanac) -> SeedLocator:
    return SeedLocator.from_almanac(almanac)


def test_self_lookup_returns_self(seed_locator: SeedLocator) -> None:
    seed = seed_locator.seed(3)
    assert seed["seed"] == seed


def test_raise_error_on_missing_lookup(seed_locator: SeedLocator) -> None:
    with pytest.raises(ValueError, match="^'missing' is not in list$"):
        seed_locator.seed(3)["missing"]


def test_return_same_number_for_next_category_outside_range(
    seed_locator: SeedLocator,
) -> None:
    seed = seed_locator.seed(3)
    assert seed["soil"] == seed_locator.number("soil", 3)


def test_return_mapped_number_for_next_category_in_range(
    seed_locator: SeedLocator,
) -> None:
    seed = seed_locator.seed(50)
    assert seed["soil"] == seed_locator.number("soil", 52)


def test_return_number_for_two_categories_down(seed_locator: SeedLocator) -> None:
    seed = seed_locator.seed(79)
    assert seed["fertilizer"] == seed_locator.number("fertilizer", 81)


def test_raise_error_on_backwards_lookup(seed_locator: SeedLocator) -> None:
    number = seed_locator.number("fertilizer", 81)
    with pytest.raises(ValueError, match="^'seed' precedes in list$"):
        number["seed"]


def test_return_location_number(seed_locator: SeedLocator) -> None:
    seed = seed_locator.seed(79)
    assert seed["location"] == seed_locator.number("location", 82)


def test_list_all_numbers_for_seed(seed_locator: SeedLocator) -> None:
    seed = seed_locator.seed(79)
    assert list(seed_locator.iter_mappings(seed)) == [
        seed,
        seed_locator.number(category="soil", value=81),
        seed_locator.number(category="fertilizer", value=81),
        seed_locator.number(category="water", value=81),
        seed_locator.number(category="light", value=74),
        seed_locator.number(category="temperature", value=78),
        seed_locator.number(category="humidity", value=78),
        seed_locator.number(category="location", value=82),
    ]


def test_seed_locator(seed_locator: SeedLocator) -> None:
    assert seed_locator.lowest_location_number() == 35
