import numpy as np
import copy
import time

mono = [
        [[ 3,  2,  1,  0],[ 2,  1,  0, -1],[ 1,  0, -1, -2],[ 0, -1, -2, -3]],
		[[ 0,  1,  2,  3],[-1,  0,  1,  2],[-2, -1,  0,  1],[-3, -2, -1, -0]],
		[[ 0, -1, -2, -3],[ 1,  0, -1, -2],[ 2,  1,  0, -1],[ 3,  2,  1,  0]],
		[[-3, -2, -1,  0],[-2, -1,  0,  1],[-1,  0,  1,  2],[ 0,  1,  2,  3]]
        ]

actions = ['Left', 'Up', 'Right', 'Down']

def Decision(grid, Max=True):
    limit = 4
    start = time.clock()

    if Max:
        return Maximize(grid, -np.inf, np.inf, limit, start)
    else:
        return Minimize(grid, -np.inf, np.inf, limit, start)

def Maximize(grid, alpha, beta, depth, start):
    if grid.terminal() or depth==0 or (time.clock()-start)>0.04:
        return grid.get_mono_score()

    maxUtility =  -np.inf

    for move in grid.get_available_moves():
        child = grid.move(move)
        maxUtility = max(maxUtility, Minimize(child, alpha, beta, depth - 1, start))

        if maxUtility >= beta:
        	break

        alpha = max(maxUtility, alpha)

    return maxUtility

def Minimize(grid, alpha, beta, depth, start):
    if grid.terminal() or depth==0 or (time.clock()-start)>0.04:
        return grid.get_mono_score()

    minUtility = np.inf 

    empty = grid.get_available_cells()

    children = []

    for i, j in empty:
        grid_2 = Grid(copy.deepcopy(grid.grid))
        grid_4 = Grid(copy.deepcopy(grid.grid))

        grid_2.grid[i][j] = 2
        grid_4.grid[i][j] = 4

        children.append(grid_2)
        children.append(grid_4)

    for child in children:
        minUtility = min(minUtility, Maximize(child, alpha, beta, depth - 1, start))

        if minUtility <= alpha:
            break

        beta = min(minUtility, beta)

    return minUtility

class Grid(object):
    def __init__(self, grid):
        self.grid = grid

    def get_available_cells(self):
        cells = []

        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    cells.append((i, j))
        
        return cells

    def get_available_moves(self):
        moves = []
        count = 0

        for action in actions:
            temp = np.rot90(np.array(self.grid), count)
            count += 1
            x = 0

            for row in temp:
                for i in range(3):
                    if row[i] == 0 and row[i + 1] != 0:
                        moves.append(action)
                        x = 1
                        break

                    if row[i] != 0 and row[i] == row[i + 1]:
                        moves.append(action)
                        x = 1
                        break
                
                if x == 1:
                    break
            
        return moves
    
    def terminal(self):
        return not self.get_available_moves()

    def move(self, dir):
        def tight(grid):
            temp = []
            for row in grid:
                new = [i for i in row if i != 0]
                new += [0 for i in range(4 - len(new))]
                temp.append(new)

            return temp

        def merge(grid):
            pair = False
            temp = []
            for row in grid:
                new = []
                for i in range(4):
                    if not pair:
                        if i + 1 < 4 and row[i] == row[i + 1]:
                            pair = True
                        else:
                            new.append(row[i])
                    else:
                        new.append(2 * row[i])
                        new.append(0)
                        pair = False

                temp.append(new)

            return temp
        
        for i in range(4):
            if dir == actions[i]:
                count = i
                break

        temp = np.rot90(np.array(self.grid), count).tolist()

        temp = tight(merge(tight(temp)))

        return Grid(np.rot90(np.array(temp), -count).tolist())

    def get_mono_score(self):
        if self.terminal():
            return -np.inf

        values = [0,0,0,0]

        for i in range(4):
            for x in range(4):
                for y in range(4):
                    values[i] += mono[i][x][y]*self.grid[x][y]
        
        return max(values)

class AI(object):
    def get_move(self, field):
        grid = Grid(field)
        maxUtility = -np.inf
        nextDir = -1

        for move in grid.get_available_moves():
            child = grid.move(move)

            utility = Decision(child, False)

            if maxUtility <= utility:
                maxUtility = utility
                nextDir = move
        
        return nextDir
