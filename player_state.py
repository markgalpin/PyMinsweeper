""" 
This will be the player's board state
"""
__author__ = 'Mark Galpin'
__version__ = '0.1'

from play_grid import VisibleValue
from player_cell import PlayerCell

class CellBlock:
    cell: PlayerCell = None
    potentials: list[PlayerCell] = []
    #TODO: I may need a separate check to see if two cell blocks have full overlap in potentials.  But I may just be able to use contains

class PlayerState:
    """This class exists to let the player run hypothetical scenarios, and gives full firewall betweeen the boards
        e.g. the "player" knows only what is truly revealed on the board."""
    my_grid: list[list[PlayerCell]] = []
    count_unrevealed:   int = 0
    count_total:        int = 0
    num_cols:           int = 0
    num_rows:           int = 0
    def __init__(self, ascii_game_board: list[str], num_rows, num_cols):
        if self.populate_my_grid(ascii_game_board):
            return None
        else:
            self.num_cols=num_cols
            self.num_rows=num_rows
            return self
    
    def populate_my_grid(self, ascii_game_board) -> bool:
        self.count_total = 0
        self.count_unrevealed = 0
        for row_index, row in enumerate(ascii_game_board):
            self.my_grid.append([])
            for col_index, element in enumerate(row):
                match element:
                    case '.':
                        self.my_grid[row_index][col_index]=PlayerCell(VisibleValue(is_flagged=False, is_revealed=True, value=0), row_index, col_index)
                    case '=':
                        self.my_grid[row_index][col_index]=PlayerCell(VisibleValue(is_flagged=False, is_revealed=False, value=None), row_index, col_index)
                        self.count_unrevealed+=1
                    case 'F':
                        self.my_grid[row_index][col_index]=PlayerCell(VisibleValue(is_flagged=True, is_revealed=False, value=None), row_index, col_index)
                    case 'X':
                        return True
                    case '*':
                        return True
                    case '@':
                        return True
                    case _:
                        self.my_grid[row_index][col_index]=PlayerCell(VisibleValue(is_flagged=False, is_revealed=True, value=int(element)), row_index, col_index)
                self.count_total+=1
        return False
    
    def _collect_surrounds(self, cell: PlayerCell) -> list[PlayerCell]:
        """This function returns all the surrounding cells
        NOTE: One thing I dislike about this is that it is essentially cut'n'paste from the one in play_grid.
        That said, it would be a lot of OOD infrastructure to change that, and I'm not at all sure its worth it for such a simple thing"""
        row=cell.row_index
        col=cell.col_index
        assert row >= 0 and row < self.num_rows, "Row must be in bounds"
        assert col >= 0 and col < self.num_cols, "Column must be in bounds"
        result: list[PlayerCell]=[]
        if row != 0:
            if col != 0:
                result.append(self.my_grid[row-1][col-1]) #top left
            result.append(self.my_grid[row-1][col]) #top middle
            if col != (self.num_cols-1):
                result.append(self.my_grid[row-1][col+1]) #top right
        if col!=0:
            result.append(self.my_grid[row][col-1]) #middle left
        #skip self
        if col!=(self.num_cols-1):
            result.append(self.my_grid[row][col+1]) #middle right
        if row!=(self.num_rows-1):
            if col != 0:
                result.append(self.my_grid[row+1][col-1]) #bottom left
            result.append(self.my_grid[row+1][col]) #bottom middle
            if col != (self.num_cols-1):
                result.append(self.my_grid[row+1][col+1]) #bottom right
        return result
    
    def get_block(self, row_i: int, col_i: int) -> CellBlock:
        "This returns a cell, and its unrevealed and unflagged counterparts, as well as updating"
        "a hypothetical value of the cell which equals its actual cell - number of flags."
        assert row_i >= 0 and row_i < self.num_rows, "Row must be in bounds"
        assert col_i >= 0 and col_i < self.num_cols, "Column must be in bounds"
        result = CellBlock()
        result.cell = self.my_grid[row_i][col_i]
        surrounds: list[PlayerCell] = self._collect_surrounds(result.cell)
        for cell in surrounds:
            if not cell.value.is_revealed:
                if cell.value.is_flagged:
                    result.cell.hypothetical_value-=1
                else:
                    result.potentials.append(cell)
        result.cell.is_cell_active() #since we updated the hypothetical value, we should update the active state of the cell
        if result.potentials.__len__ != 0:
            result.cell.is_active=True #This makes sure the trivial reveal rule is triggered.
        return result