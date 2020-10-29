'''
input:
data = {"start-cell": null,
        "end-cell": null,
        "walls": [],
        "rows": ROWS,
        "columns": COLUMNS};

output:
List with searched node in order
List with closest path (empty if no path is found)
'''
from collections import deque
import json


## BOARD
class Cell():
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.neighbors = []
        self.isWall = False

    def cell_str(self):
        return str(self.row) + ":" + str(self.column)


class Board():
    def __init__(self, rows, columns, walls):
        self.board = []
        self.rows = rows
        self.columns = columns

        # Create board
        for row in range(self.rows):
            self.board.append([])
            for column in range(self.columns):
                self.board[row].append(Cell(row, column))
        
        # Add walls
        for wall in walls:
            print(self.board[wall[0]][wall[1]].row, self.board[wall[0]][wall[1]].column)
            self.board[wall[0]][wall[1]].isWall = True

        # Find neighbors
        for row in self.board:
            for cell in row:
                if cell.row > 0 and not self.board[cell.row - 1][cell.column].isWall:
                    cell.neighbors.append([cell.row - 1, cell.column])
                if cell.row < self.rows - 1 and not self.board[cell.row + 1][cell.column].isWall:
                    cell.neighbors.append([cell.row + 1, cell.column])
                if cell.column > 0 and not self.board[cell.row][cell.column - 1].isWall:
                    cell.neighbors.append([cell.row, cell.column - 1])
                if cell.column < self.columns - 1 and not self.board[cell.row][cell.column + 1].isWall:
                    cell.neighbors.append([cell.row, cell.column + 1])
        
    def get_board(self):
        return self.board

    def __str__(self):
        s = ""
        for row in self.board:
            s += "\n| "
            for cell in row:
                if cell.isWall:
                    s += "x "
                else:
                    s += "o "
            s += "|"

        return s


## ALGORITHMS
class AlgorithmBase():
    def __init__(self):
        self.evaluated_cells = []

    def cell_to_str(self, cell):
        return str(cell[0]) + ":" + str(cell[1])
    
    def str_to_cell(self, s):
        cell = s.split(":")
        return [int(cell[0]), int(cell[1])]

class BFS(AlgorithmBase):
    # Implemented from wikipedias pseudocode
    def BFS(self, board, start_cell, end_cell):
        Q = deque()
        discovered = {self.cell_to_str(start_cell)}
        Q.append(start_cell)

        while Q:
            v = Q.popleft()
            self.evaluated_cells.append(v)
            
            if v == end_cell:
                return v, self.evaluated_cells
            for neighbor in board[v[0]][v[1]].neighbors:
                cell_str = board[neighbor[0]][neighbor[1]].cell_str()
                if cell_str not in discovered:
                    discovered.add(cell_str)
                    Q.append(neighbor)
        
        return [], self.evaluated_cells

class DFS(AlgorithmBase):
    # Implemented from wikipedias pseudocode
    def DFS(self, board, start_cell, end_cell):
        S = deque()
        discovered = {self.cell_to_str(start_cell)}
        S.append(start_cell)

        while S:
            v = S.pop()
            self.evaluated_cells.append(v)
            
            if v == end_cell:
                return v, self.evaluated_cells
            cell_str = board[v[0]][v[1]]
            if cell_str not in discovered:
                discovered.add(cell_str)
                for neighbor in board[v[0]][v[1]].neighbors:
                    S.append(neighbor)
        
        return [], self.evaluated_cells
    
class Astar(AlgorithmBase):
    # Implemented from wikipedias pseudocode
    def _h(self, cell):
        # Minimum possible distance
        return abs(self.end_cell[0] - cell[0]) + abs(self.end_cell[1] - cell[1])

    @staticmethod
    def _d(current, neighbor):
        return abs(current[0] - neighbor[0] + current[1] - neighbor[1])

    def _reconstruct_path(self, cameFrom, current_str):
        total_path = deque([self.str_to_cell(current_str)])
        while current_str in cameFrom:
            current_str = cameFrom[current_str]
            total_path.appendleft(self.str_to_cell(current_str))
        return list(total_path)

    def Astar(self, board, start_cell, end_cell, maxRows, maxColumns):
        self.end_cell = end_cell
        inf = 0xFFFFFFFF  # 32bit

        start = self.cell_to_str(start_cell)
        openSet = {start}

        cameFrom = {}

        # Create map with all cells as keys and infinity values
        gScore = {self.cell_to_str([row, column]): inf for column in range(maxColumns) for row in range(maxRows)}
        fScore = dict(gScore)
        gScore[start] = 0
        fScore[start] = self._h(start_cell)

        while openSet:
            # Get all fScores from open set
            openSet_fScores = {key: fScore[key] for key in openSet}

            # Get cell from open set with minimum fScore
            current_str = min(openSet_fScores, key=fScore.get)
            current = self.str_to_cell(current_str)
            self.evaluated_cells.append(current)

            # Check if goal is found
            if current == end_cell:
                return self._reconstruct_path(cameFrom, current_str), self.evaluated_cells

            openSet.remove(current_str)
            for neighbor in board[current[0]][current[1]].neighbors:
                tentative_gScore = gScore[current_str] + self._d(current, neighbor)
                neighbor_str = self.cell_to_str(neighbor)

                if tentative_gScore < gScore[neighbor_str]:
                    cameFrom[neighbor_str] = current_str
                    gScore[neighbor_str] = tentative_gScore
                    fScore[neighbor_str] = gScore[neighbor_str] + self._h(neighbor)

                    if neighbor_str not in openSet:
                        openSet.add(neighbor_str)
        
        # No solution found
        return [], self.evaluated_cells

## INTERFACE
def get_stuff(alg_type, data):
    # Convert data to dict
    data = json.loads(data)

    # Create board
    board = Board(data["rows"], data["columns"], data["walls"]).get_board()

    # Run BFS with board
    print(alg_type)
    if alg_type == "BFS":
        (solution, steps) = BFS().BFS(board, data["start-cell"], data["end-cell"])
    elif alg_type == "DFS":
        (solution, steps) = DFS().DFS(board, data["start-cell"], data["end-cell"])
    elif alg_type == "Astar":
        (solution, steps) = Astar().Astar(board, data["start-cell"], data["end-cell"], data["rows"], data["columns"])

    return {"solution": solution, "steps": steps}


# Debug
if __name__ == "__main__":
    start_cell = [0, 0]
    end_cell = [5, 5]
    rows = 6
    columns = 6
    walls = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

    board = Board(rows, columns, walls)
    print(board)

    #a, b = BFS().BFS(board.get_board(), start_cell, end_cell)
    a, b = Astar().Astar(board.get_board(), start_cell, end_cell, rows, columns)

    print(a)
    #print(b)