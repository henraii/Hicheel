# grid_world.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator
import random

DIRECTIONS_4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIRECTIONS_8 = DIRECTIONS_4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

@dataclass
class GridWorld:
    grid: list[list[str]]
    diagonal: bool = False
    step_cost: float = 1.0
    start: tuple[int, int] = field(init=False)
    goal: tuple[int, int] = field(init=False)

    def __post_init__(self):
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = self._find('S')
        self.goal = self._find('G')

    def _find(self, symbol: str) -> tuple[int, int]:
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if val == symbol:
                    return (r, c)
        raise ValueError(f"'{symbol}' олдсонгүй")

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, r: int, c: int) -> bool:
        return self.grid[r][c] != '#'

    def neighbors(self, pos: tuple[int, int]) -> Iterator[tuple[int, int, float]]:
        r, c = pos
        dirs = DIRECTIONS_8 if self.diagonal else DIRECTIONS_4
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.is_free(nr, nc):
                cost = self.step_cost * (1.4142 if dr and dc else 1.0)
                yield (nr, nc, cost)

    @classmethod
    def random(cls, rows: int, cols: int, obstacle_p: float = 0.25,
               seed: int | None = None, diagonal: bool = False):
        rng = random.Random(seed)
        g = [['#' if rng.random() < obstacle_p else '.' for _ in range(cols)]
             for _ in range(rows)]
        g[0][0] = 'S'
        g[rows-1][cols-1] = 'G'
        return cls(g, diagonal=diagonal)
