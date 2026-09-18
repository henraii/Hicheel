from pyamaze import maze, agent, COLOR, textLabel
from collections import deque
def BFS(m):
    start = (m.rows, m.cols)
    explored = [start]
    frontier = deque([start])
    bfsPath = {}
    while len(frontier) > 0:
        currentCell = frontier.popleft()
        if currentCell == (1, 1):
            break
        for d in 'ESNW':
            if m.maze_map[currentCell][d] == True:
                if d == 'E':
                    childCell = (currentCell[0], currentCell[1] + 1)
                if d == 'W':
                    childCell = (currentCell[0], currentCell[1] - 1)
                if d == 'N':
                    childCell = (currentCell[0] - 1, currentCell[1])
                if d == 'S':
                    childCell = (currentCell[0] + 1, currentCell[1])
                if childCell in explored:
                    continue
                explored.append(childCell)
                frontier.append(childCell)
                bfsPath[childCell] = currentCell
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    return fwdPath
if __name__ == '__main__':
    m = maze(5,5)
    m.CreateMaze(loopPercent=100)
    path = BFS(m)

    a = agent(m, footprints=True, filled=True, color=COLOR.red, shape='arrow')
    m.tracePath({a: path})
    l=textLabel(m, 'Length of shortest path from start to goal:', len(path)+1)

    m.run()
