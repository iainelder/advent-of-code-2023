from pathlib import Path
from typing import Iterable, TypedDict

import geopandas as gpd  # type: ignore[import-untyped]
from lark import Lark, Token
from shapely import Polygon  # type: ignore[import-untyped]


class _TokenPoly(TypedDict):
    token: Token
    poly: Polygon


class Schematic:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.parser = Lark(GRAMMAR)

    def part_sum(self) -> int:
        gdf = self.data_frame()
        symbols = gdf[gdf["token"].apply(lambda x: x.type) == "SYMBOL"]
        numbers = gdf[gdf["token"].apply(lambda x: x.type) == "INT"]
        return int(
            symbols.sjoin(numbers)["token_right"].apply(lambda t: int(t.value)).sum()
        )

    def iter_tokens(self) -> Iterable[Token]:
        for token in self.parser.lex(self.path.read_text()):
            yield token

    def data_frame(self) -> gpd.GeoDataFrame:
        gdf = gpd.GeoDataFrame(self._iter_token_polys(), columns=["token", "poly"])
        gdf.set_geometry("poly", inplace=True)
        return gdf

    def _iter_token_polys(self) -> Iterable[_TokenPoly]:
        for token in self.iter_tokens():
            yield _TokenPoly(token=token, poly=Schematic.polygon(token))

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
SYMBOL: "*"|"#"|"+"|"$"
SPACE: "."
%import common.INT
%import common.NEWLINE
%ignore SPACE
%ignore NEWLINE
"""
