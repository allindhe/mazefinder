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
class BFS():
    def __init__(self):
        self.evaluated_cells = []

    def cell_to_str(self, cell):
        return str(cell[0]) + ":" + str(cell[1])

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


## INTERFACE
def get_stuff(alg_type, data):
    # Convert data to dict
    data = json.loads(data)

    # Create board
    print(data)
    board = Board(data["rows"], data["columns"], data["walls"]).get_board()

    # Run BFS with board
    (solution, steps) = BFS().BFS(board, data["start-cell"], data["end-cell"])

    print(solution)
    print(steps)
    return {"solution": solution, "steps": steps}


# Debug
if __name__ == "__main__":
    start_cell = [0, 0]
    end_cell = [29, 29]
    rows = 30
    columns = 30
    walls = [[0, 5], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

    board = Board(rows, columns, walls)
    print(board)

    a, b = BFS().BFS(board.get_board(), start_cell, end_cell)
    print(a)
    print(b)