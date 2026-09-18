from pyamaze import maze, agent, COLOR


def DFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    explored = [start]
    frontier = [start]
    dfsPath = {}

    while frontier:
        currCell = frontier.pop()

        if currCell == m._goal:
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                if childCell in explored:
                    continue

                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell

    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]

    return fwdPath


if __name__ == '__main__':
    m = maze(5, 5)
    m.CreateMaze()

    path = DFS(m)

    a = agent(m, footprints=True, color=COLOR.red)
    m.tracePath({a: path})

    m.run()
