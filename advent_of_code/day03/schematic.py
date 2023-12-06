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

    def part_sum(self) -> int:
        gdf = self.data_frame()
        symbols = gdf[gdf["type"] == "SYMBOL"]
        numbers = gdf[gdf["type"] == "INT"]
        return int(symbols.sjoin(numbers)["text_right"].astype(int).sum())

    def gear_ratio_sum(self) -> int:
        gdf = self.data_frame()
        stars = gdf[gdf["text"] == "*"]
        numbers = gdf[gdf["type"] == "INT"]

        answer = int(
            stars.sjoin(numbers)["text_right"]
            .astype(int)
            .groupby(level=0)
            .agg(["size", "prod"])
            .query("size == 2")["prod"]
            .sum()
        )

        return answer

    def iter_tokens(self) -> Iterable[Token]:
        yield from Lark(GRAMMAR).lex(self.path.read_text())

    def data_frame(self) -> gpd.GeoDataFrame:
        gdf = gpd.GeoDataFrame(self.iter_spatial_tokens())
        gdf.set_geometry("polygon", inplace=True)
        gdf.rename_axis("ID", axis="columns", inplace=True)
        return gdf

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
