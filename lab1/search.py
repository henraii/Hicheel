# search.py
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from heapq import heappush, heappop
from itertools import count
from typing import Callable, Literal
from grid_world import GridWorld

Pos = tuple[int, int]
Heuristic = Callable[[Pos, Pos], float]


def manhattan(a: Pos, b: Pos) -> float:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a: Pos, b: Pos) -> float:
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

def chebyshev(a: Pos, b: Pos) -> float:
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def zero(a: Pos, b: Pos) -> float:
    return 0.0


@dataclass
class SearchResult:
    algorithm: str
    found: bool
    path: list[Pos]
    visited_order: list[Pos]
    frontier_peak: int
    total_cost: float = 0.0
    expanded: int = 0
    heuristic_name: str = "—"

    @property
    def path_length(self) -> int:
        return len(self.path) - 1 if self.found else -1

    @property
    def visited_count(self) -> int:
        return len(self.visited_order)


def _reconstruct(parent: dict, goal: Pos) -> list[Pos]:
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]


def _search_bfs_dfs(grid: GridWorld, strategy: Literal["bfs", "dfs"]) -> SearchResult:
    start, goal = grid.start, grid.goal
    frontier = deque([start]) if strategy == "bfs" else [start]
    visited = {start}
    parent = {start: None}
    order: list[Pos] = []
    peak = 1

    while frontier:
        peak = max(peak, len(frontier))
        cur = frontier.popleft() if strategy == "bfs" else frontier.pop()
        order.append(cur)

        if cur == goal:
            path = _reconstruct(parent, goal)
            return SearchResult(strategy.upper(), True, path, order, peak,
                                total_cost=float(len(path) - 1),
                                expanded=len(order))

        for nr, nc, _ in grid.neighbors(cur):
            nbr = (nr, nc)
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = cur
                frontier.append(nbr)

    return SearchResult(strategy.upper(), False, [], order, peak, expanded=len(order))


def _search_informed(grid: GridWorld, algorithm: Literal["gbfs", "astar"],
                     h: Heuristic) -> SearchResult:
    start, goal = grid.start, grid.goal
    counter = count()                      # tie-breaker
    frontier: list = []
    heappush(frontier, (0.0, next(counter), start))
    g: dict[Pos, float] = {start: 0.0}
    parent: dict[Pos, Pos | None] = {start: None}
    closed: set[Pos] = set()
    order: list[Pos] = []
    peak = 1

    while frontier:
        peak = max(peak, len(frontier))
        _, _, cur = heappop(frontier)

        if cur in closed:
            continue
        closed.add(cur)
        order.append(cur)

        if cur == goal:
            path = _reconstruct(parent, goal)
            return SearchResult(algorithm.upper(), True, path, order, peak,
                                total_cost=g[goal], expanded=len(order),
                                heuristic_name=h.__name__)

        for nr, nc, step in grid.neighbors(cur):
            nbr = (nr, nc)
            if nbr in closed:
                continue
            tentative_g = g[cur] + step

            if algorithm == "gbfs":
                if nbr not in g:
                    g[nbr] = tentative_g
                    parent[nbr] = cur
                    heappush(frontier, (h(nbr, goal), next(counter), nbr))
            else:                                    # astar
                if nbr not in g or tentative_g < g[nbr]:
                    g[nbr] = tentative_g
                    parent[nbr] = cur
                    f = tentative_g + h(nbr, goal)
                    heappush(frontier, (f, next(counter), nbr))

    return SearchResult(algorithm.upper(), False, [], order, peak,
                        expanded=len(order), heuristic_name=h.__name__)


def bfs(grid: GridWorld) -> SearchResult:
    return _search_bfs_dfs(grid, "bfs")

def dfs(grid: GridWorld) -> SearchResult:
    return _search_bfs_dfs(grid, "dfs")

def gbfs(grid: GridWorld, h: Heuristic = manhattan) -> SearchResult:
    return _search_informed(grid, "gbfs", h)

def astar(grid: GridWorld, h: Heuristic = manhattan) -> SearchResult:
    return _search_informed(grid, "astar", h)
