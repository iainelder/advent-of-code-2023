from pathlib import Path
import pytest
from advent_of_code.day05.almanac import Almanac, Number

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
    assert almanac.lowest_location_number() == location_number


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


def test_self_lookup_returns_self(almanac: Almanac) -> None:
    seed = almanac.seed(3)
    assert seed["seed"] == seed


def test_raise_error_on_missing_lookup(almanac: Almanac) -> None:
    with pytest.raises(ValueError, match="^'missing' is not in list$"):
        almanac.seed(3)["missing"]


def test_return_same_number_for_next_category_outside_range(almanac: Almanac) -> None:
    seed = almanac.seed(3)
    assert seed["soil"] == Number(category="soil", value=3, almanac=almanac)


def test_return_mapped_number_for_next_category_in_range(almanac: Almanac) -> None:
    seed = almanac.seed(50)
    assert seed["soil"] == Number(category="soil", value=52, almanac=almanac)


def test_return_number_for_two_categories_down(almanac: Almanac) -> None:
    seed = almanac.seed(79)
    assert seed["fertilizer"] == Number(
        category="fertilizer", value=81, almanac=almanac
    )


def test_raise_error_on_backwards_lookup(almanac: Almanac) -> None:
    number = Number(category="fertilizer", value=81, almanac=almanac)
    with pytest.raises(ValueError, match="^'seed' precedes in list$"):
        number["seed"]


def test_return_location_number(almanac: Almanac) -> None:
    seed = almanac.seed(79)
    assert seed["location"] == Number(category="location", value=82, almanac=almanac)


def test_list_all_numbers_for_seed(almanac: Almanac) -> None:
    seed = almanac.seed(79)
    assert list(almanac.iter_mappings(seed)) == [
        seed,
        almanac.number(category="soil", value=81),
        almanac.number(category="fertilizer", value=81),
        almanac.number(category="water", value=81),
        almanac.number(category="light", value=74),
        almanac.number(category="temperature", value=78),
        almanac.number(category="humidity", value=78),
        almanac.number(category="location", value=82),
    ]
