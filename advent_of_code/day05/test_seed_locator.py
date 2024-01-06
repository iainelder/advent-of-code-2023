import pytest
from advent_of_code.day05.seed_locator import SeedLocator


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
