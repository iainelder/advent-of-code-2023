from advent_of_code.day05.range_locator import RangeLocator


def test_disjoint_range_breaks_down_to_self(range_locator: RangeLocator) -> None:
    seed_range = range_locator.seed(0, 10)
    assert seed_range.break_down() == [seed_range]


# TODO: More tests
