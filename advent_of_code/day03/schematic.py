from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import geopandas as gpd  # type: ignore[import-untyped]
from lark import Lark, Token
from shapely import Polygon  # type: ignore[import-untyped]


@dataclass
class SpatialToken:
    polygon: Polygon
    type: str
    text: str


class Schematic:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.symbols, self.numbers = self.build_data_frames()

    def part_sum(self) -> int:
        return sum(self.symbols.sjoin(self.numbers)["value"])

    def gear_ratio_sum(self) -> int:
        stars = self.symbols[self.symbols["text"] == "*"]

        return sum(
            stars.sjoin(self.numbers)["value"]
            .groupby(level=0)
            .agg(["size", "prod"])
            .query("size == 2")["prod"]
        )

    def iter_tokens(self) -> Iterable[Token]:
        yield from Lark(GRAMMAR).lex(self.path.read_text())

    def build_data_frames(self) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
        gdf = gpd.GeoDataFrame(self.iter_spatial_tokens()).set_geometry("polygon")
        symbols = gdf[gdf["type"] == "SYMBOL"][["polygon", "text"]]
        numbers = (
            gdf[gdf["type"] == "INT"][["polygon", "text"]]
            .astype({"text": int})
            .rename(columns={"text": "value"})
        )
        return symbols, numbers

    def iter_spatial_tokens(self) -> Iterable[SpatialToken]:
        for token in self.iter_tokens():
            yield SpatialToken(
                polygon=Schematic.polygon(token),
                type=token.type,
                text=token.value,
            )

    @staticmethod
    def polygon(token: Token) -> Polygon:
        assert isinstance(token.line, int)
        assert isinstance(token.column, int)
        assert isinstance(token.end_column, int)

        coords = (
            (token.line, token.column),
            (token.line, token.end_column),
            (token.line + 1, token.end_column),
            (token.line + 1, token.column),
            (token.line, token.column),
        )
        return Polygon(coords)


GRAMMAR = r"""
start: [INT|SYMBOL]*
SYMBOL: "*"|"#"|"+"|"$"|"-"|"%"|"/"|"&"|"="|"@"
SPACE: "."
%import common.INT
%import common.NEWLINE
%ignore SPACE
%ignore NEWLINE
"""
