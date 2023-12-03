from pathlib import Path


class Schematic:
    def __init__(self, path: Path) -> None:
        self.path = path

    def part_sum(self) -> int:
        return 0
