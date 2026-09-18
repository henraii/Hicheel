# benchmark.py
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from grid_world import GridWorld
from search import bfs, dfs, gbfs, astar, manhattan

SIZES = [5, 10, 15, 20, 25]
TRIALS = 10
OBSTACLE_P = 0.25

ALGOS = {
    "BFS":  lambda g: bfs(g),
    "DFS":  lambda g: dfs(g),
    "GBFS": lambda g: gbfs(g, manhattan),
    "A*":   lambda g: astar(g, manhattan),
}
COLORS = {"BFS": "#2a78d6", "DFS": "#eb6834", "GBFS": "#1baf7a", "A*": "#eda100"}
MARKERS = {"BFS": "o", "DFS": "s", "GBFS": "^", "A*": "D"}


def run():
    visited = {n: [] for n in ALGOS}
    times   = {n: [] for n in ALGOS}
    costs   = {n: [] for n in ALGOS}
    solvable = []

    for n in SIZES:
        found_count = 0
        for name, fn in ALGOS.items():
            v, t, c = [], [], []
            for trial in range(TRIALS):
                g = GridWorld.random(n, n, obstacle_p=OBSTACLE_P, seed=trial)
                t0 = time.perf_counter()
                res = fn(g)
                dt = (time.perf_counter() - t0) * 1000
                if res.found:
                    v.append(res.visited_count)
                    t.append(dt)
                    c.append(res.total_cost)
            visited[name].append(np.mean(v) if v else float('nan'))
            times[name].append(np.mean(t) if t else float('nan'))
            costs[name].append(np.mean(c) if c else float('nan'))
            found_count = max(found_count, len(v))
        solvable.append(found_count)

    return visited, times, costs, solvable


def plot(visited, times, costs, path="results/comparison.png"):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    series = [(visited, "Avg visited nodes", "Visited nodes"),
              (times,   "Avg time (ms)",     "Execution time"),
              (costs,   "Avg path cost",     "Path cost (optimality)")]

    for ax, (data, ylabel, title) in zip(axes, series):
        for name in ALGOS:
            ax.plot(SIZES, data[name], marker=MARKERS[name], markersize=6,
                    linewidth=2, color=COLORS[name], label=name)
        ax.set_xlabel("Grid size (n×n)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(SIZES)
        ax.grid(True, alpha=0.25, linewidth=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    axes[0].legend(frameon=False)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    return path


if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    visited, times, costs, solvable = run()

    hdr = f"{'Grid':>7} | " + " | ".join(f"{n:>8}" for n in ALGOS)
    print("Avg visited nodes (10 trials, obstacle_p=0.25)")
    print(hdr); print("-" * len(hdr))
    for i, n in enumerate(SIZES):
        print(f"{n:>3}x{n:<3} | " + " | ".join(f"{visited[a][i]:8.1f}" for a in ALGOS))

    print("\nAvg time (ms)")
    print(hdr); print("-" * len(hdr))
    for i, n in enumerate(SIZES):
        print(f"{n:>3}x{n:<3} | " + " | ".join(f"{times[a][i]:8.3f}" for a in ALGOS))

    print("\nAvg path cost")
    print(hdr); print("-" * len(hdr))
    for i, n in enumerate(SIZES):
        print(f"{n:>3}x{n:<3} | " + " | ".join(f"{costs[a][i]:8.1f}" for a in ALGOS))

    print(f"\nSolvable grids per size (of {TRIALS}):",
          {n: s for n, s in zip(SIZES, solvable)})
    print("chart ->", plot(visited, times, costs))
