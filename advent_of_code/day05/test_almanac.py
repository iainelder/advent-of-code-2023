from advent_of_code.day05.almanac import Almanac, Map, MapRange


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


def test_almanac_has_map(almanac: Almanac) -> None:
    assert almanac.maps[0:2] == [
        Map(
            source="seed",
            dest="soil",
            ranges=[
                MapRange(dest_start=50, source_start=98, source_length=2),
                MapRange(dest_start=52, source_start=50, source_length=48),
            ],
        ),
        Map(
            source="soil",
            dest="fertilizer",
            ranges=[
                MapRange(dest_start=0, source_start=15, source_length=37),
                MapRange(dest_start=37, source_start=52, source_length=2),
                MapRange(dest_start=39, source_start=0, source_length=15),
            ],
        ),
    ]
