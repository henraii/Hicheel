from pyamaze import maze, agent, COLOR
def DFS(m):
    start =(m.rows,m.cols)
    explored = [start]
    frontier = [start]
    dfsPath = {}
    while len(frontier) > 0:
        currentCell =frontier.pop()
        if currentCell == (1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currentCell][d] == True:
                if d == 'E':
                    childCell = (currentCell[0], currentCell[1]+1)
                if d == 'W':
                    childCell = (currentCell[0], currentCell[1]-1)
                if d == 'N':
                    childCell = (currentCell[0]-1, currentCell[1])
                if d == 'S':
                    childCell = (currentCell[0]+1, currentCell[1])
                if childCell in explored:
                    continue
                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currentCell
    fwdPath = {}
    cell = (1,1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return fwdPath

m=maze(20,20)
m.CreateMaze()
path = DFS(m)
a = agent(m, footprints=True)
m.tracePath({a:path})

m.run()