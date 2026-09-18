# test_search.py
import pytest
from grid_world import GridWorld
from search import bfs, dfs, gbfs, astar, manhattan, zero


@pytest.fixture
def simple_grid():
    return GridWorld([['S','.','.'],['.','#','.'],['.','.','G']])


def test_bfs_shortest(simple_grid):
    assert bfs(simple_grid).path_length == 4


def test_dfs_finds_path(simple_grid):
    assert dfs(simple_grid).found


def test_gbfs_finds_path(simple_grid):
    assert gbfs(simple_grid).found


def test_astar_optimal_matches_bfs(simple_grid):
    b = bfs(simple_grid).path_length
    a = astar(simple_grid).path_length
    assert a == b                      # Manhattan admissible -> optimal


def test_astar_with_zero_heuristic_is_bfs(simple_grid):
    a = astar(simple_grid, zero)
    b = bfs(simple_grid)
    assert a.path_length == b.path_length


def test_no_path():
    g = GridWorld([['S','#','G']])
    for fn in (bfs, dfs, gbfs, astar):
        assert not fn(g).found


def test_gbfs_may_be_suboptimal():
    """GBFS нь optimal биш болохыг харуулах жишээ."""
    g = GridWorld([
        ['S', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '.'],
        ['.', '.', '.', '.', 'G'],
    ])
    b = bfs(g).path_length
    gb = gbfs(g, manhattan).path_length
    assert gb >= b                     # GBFS >= BFS-ийн зам
