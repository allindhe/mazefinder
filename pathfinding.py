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
import math
import random

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
            self.board[wall[0]][wall[1]].isWall = True

        # Find neighbors
        for row in self.board:
            for cell in row:
                # Horizontal
                if cell.row > 0 and not self.board[cell.row - 1][cell.column].isWall:  # Left
                    cell.neighbors.append([cell.row - 1, cell.column])
                if cell.row < self.rows - 1 and not self.board[cell.row + 1][cell.column].isWall:  # Right
                    cell.neighbors.append([cell.row + 1, cell.column])
                if cell.column > 0 and not self.board[cell.row][cell.column - 1].isWall:  # Down
                    cell.neighbors.append([cell.row, cell.column - 1])
                if cell.column < self.columns - 1 and not self.board[cell.row][cell.column + 1].isWall:  # Up
                    cell.neighbors.append([cell.row, cell.column + 1])

                # Diagonal (Inactive for now)
                if False:
                    if cell.row > 0 and cell.column > 0 and not self.board[cell.row - 1][cell.column - 1].isWall:  # Top left
                        cell.neighbors.append([cell.row - 1, cell.column - 1])
                    if cell.row < self.rows - 1 and cell.column > 0 and not self.board[cell.row + 1][cell.column - 1].isWall:  # Top right
                        cell.neighbors.append([cell.row + 1, cell.column - 1])
                    if cell.row > 0 and cell.column < self.columns - 1 and not self.board[cell.row - 1][cell.column + 1].isWall:  # Bottom left
                        cell.neighbors.append([cell.row - 1, cell.column + 1])
                    if cell.row < self.rows - 1 and cell.column < self.columns - 1 and not self.board[cell.row + 1][cell.column + 1].isWall:  # Bottom right
                        cell.neighbors.append([cell.row + 1, cell.column + 1])


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

class AlgorithmBase():
    def __init__(self):
        self.evaluated_cells = []

    def cell_to_str(self, cell):
        return str(cell[0]) + ":" + str(cell[1])
    
    def str_to_cell(self, s):
        cell = s.split(":")
        return [int(cell[0]), int(cell[1])]

## MAZE GENERATION
class EllersAlgorithm(AlgorithmBase):
    """ Based on http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm.html """
    def __init__(self, max_rows, max_columns):
        self.max_rows = max_rows
        self.max_columns = max_columns

        # Create walls as input for creating board
        walls = []
        for row in range(self.max_rows):
            for column in range(self.max_columns):
                pass

        self.board = 0

        self.path_sets = {}
        self.cell_in_set = {}
        self.create_sets()

        self.removed_walls = []

    def create_sets(self):
        """
        Initialize sets.
        path_sets includes all the path sets
        {0: {0:0, 0:1}, 1: {1:0, 1:1, 2:0}}

        cell_in_set can lookup in which set a cell is currently in
        {"0:0": 0, "0:1": 0, "1:1": 1} etc..
        """
        idx = 0
        for row in range(1, self.max_rows, 2):
            for column in range(1, self.max_columns, 2):
                cell_str = self.cell_to_str([row, column])
                self.path_sets[idx] = {cell_str}
                self.cell_in_set[cell_str] = idx
                idx += 1

    def is_in_same_set(self, left_cell, right_cell):
        return right_cell in self.path_sets[self.cell_in_set[left_cell]]

    def remove_wall_between_cells(self, first, second):
        first_cell = self.str_to_cell(first)
        second_cell = self.str_to_cell(second)
        self.removed_walls.append([int((first_cell[0] + second_cell[0]) / 2),
                                   int((first_cell[1] + second_cell[1]) / 2)])

    def combine_two_sets(self, left_cell, right_cell):
        """ If not in same set, remove the right cell set and merge it with the left cell set """
        if not self.is_in_same_set(left_cell, right_cell):
            removed_set = self.path_sets.pop(self.cell_in_set[right_cell], None)

            cell_reference_set = self.cell_in_set[left_cell]
            self.path_sets[cell_reference_set] = self.path_sets[cell_reference_set] | removed_set
            for removed_cell in removed_set:
                self.cell_in_set[removed_cell] = cell_reference_set

            # Remove the wall between the two cells
            self.remove_wall_between_cells(left_cell, right_cell)

    def create_walls(self):
        walls = []
        for row in range(self.max_rows):
            for column in range(self.max_columns):
                if row % 2 == 0 or column % 2 == 0:
                    if not [row, column] in self.removed_walls:
                        walls.append([row, column])
                
        return walls

    def generateMaze(self):
        # Loop over every other row
        for row in range(1, self.max_rows, 2):
            # Loop over every other column except last one
            for column in range(1, self.max_columns - 2, 2):
                left_cell_str = self.cell_to_str([row, column])
                right_cell_str = self.cell_to_str([row, column + 2])

                # Roll the dice and see if we should combine set with right set
                if random.random() >= 0.5:
                    self.combine_two_sets(left_cell_str, right_cell_str)

            # Check which sets are in the row
            sets_in_row = set()
            for column in range(1, self.max_columns, 2):
                sets_in_row.add(self.cell_in_set[self.cell_to_str([row, column])])

            # Create vertical connections, (all sets must have at least one connection)
            sets_with_vertical_connections = set()
            if row < self.max_rows - 2:
                # Loop over every other column. This is gonna be fugly
                for column in range(1, self.max_columns, 2):
                    top_cell_str = self.cell_to_str([row, column])
                    bottom_cell_str = self.cell_to_str([row + 2, column])
                    current_set = self.cell_in_set[top_cell_str]

                    if random.random() >= 0.5:
                        self.combine_two_sets(top_cell_str, bottom_cell_str)
                        sets_with_vertical_connections.add(current_set)

                # If all sets don't have a vertical connection
                for _ in range(1000):  # Instead of while
                    for column in range(1, self.max_columns, 2):
                        top_cell_str = self.cell_to_str([row, column])
                        bottom_cell_str = self.cell_to_str([row + 2, column])
                        current_set = self.cell_in_set[top_cell_str]
                        if current_set not in sets_with_vertical_connections:
                            if random.random() >= 0.5:
                                self.combine_two_sets(top_cell_str, bottom_cell_str)
                                sets_with_vertical_connections.add(current_set)

                    if len(sets_in_row) <= len(sets_with_vertical_connections):
                        break
            else:  # Last row
                # Join all disjoint sets
                for column in range(1, self.max_columns - 2, 2):
                    left_cell_str = self.cell_to_str([row, column])
                    right_cell_str = self.cell_to_str([row, column + 2])
                    self.combine_two_sets(left_cell_str, right_cell_str)

        walls = self.create_walls()
        return walls


## SEARCH ALGORITHMS
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
        return self._d(self.end_cell, cell)

    @staticmethod
    def _d(current, neighbor):
        return math.sqrt((current[0] - neighbor[0])**2 + (current[1] - neighbor[1])**2)

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
def calculate_path(alg_type, data):
    # Convert data to dict
    data = json.loads(data)

    # Create board
    board = Board(data["rows"], data["columns"], data["walls"]).get_board()

    # Run BFS with board
    if alg_type == "BFS":
        (solution, steps) = BFS().BFS(board, data["start-cell"], data["end-cell"])
    elif alg_type == "DFS":
        (solution, steps) = DFS().DFS(board, data["start-cell"], data["end-cell"])
    elif alg_type == "Astar":
        (solution, steps) = Astar().Astar(board, data["start-cell"], data["end-cell"], data["rows"], data["columns"])

    return {"solution": solution, "steps": steps}

def calculate_maze(maze_type, data):
    # Convert data to dict
    data = json.loads(data)

    # Generate walls with a maze algorithm
    if maze_type == "Ellers":
        walls = EllersAlgorithm(data["rows"], data["columns"]).generateMaze()

    return {"walls": walls}

# Debug
if __name__ == "__main__":
    start_cell = [0, 0]
    end_cell = [5, 5]
    rows = 9
    columns = 9
    walls = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

    #board = Board(rows, columns, walls)
    #print(board)

    #a, b = BFS().BFS(board.get_board(), start_cell, end_cell)
    #a, b = Astar().Astar(board.get_board(), start_cell, end_cell, rows, columns)
    walls = EllersAlgorithm(rows, columns).generateMaze()
    board = Board(rows, columns, walls)
    print(board)
    #print(a)
    #print(b)