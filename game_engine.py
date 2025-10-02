""" 
This defines the minesweeper game engine
"""
__author__ = 'Mark Galpin'
__version__ = '0.1'

DEFAULT_GRID_COLS=17
DEFAULT_GRID_ROWS=24
DEFAULT_NUM_MINES=85

from play_grid import Grid, Cell, RevealedValue, VisibleValue

class Engine:
    """Functions for modifying the grid while playing"""
    grid: Grid = None
    num_flags: int = 0
    def __init__(self, num_rows, num_cols, num_mines):
        self.grid=Grid(num_rows, num_cols, num_mines)
        return

    def mines_remaining(self) -> int:
        """Gives the number of mines remaining"""
        return self.grid.num_mines-self.num_flags

    def reveal_cell(self, row: int, col: int) -> bool:
        """reveals the cell, plus other cells if its empty.  Returns true if boom!"""
        assert row >= 0 and row < self.grid.num_rows, "Row must be in bounds"
        assert col >= 0 and col < self.grid.num_cols, "Column must be in bounds"
        result=self.grid[row][col].reveal()
        if result.is_mined:
            return True
        if result.value==0:
            surrounds=self.grid.collect_surrounds(row, col)
            for cell in surrounds:
                inner_result=self.reveal_cell(cell.row_index, cell.col_index)
                assert not inner_result
        return False

    def flag_cell(self, row: int, col: int, flag_val: bool = True) -> None:
        """Flags a cell at the specified coordinate.  pass False to unflag"""
        assert row >= 0 and row < self.grid.num_rows, "Row must be in bounds"
        assert col >= 0 and col < self.grid.num_cols, "Column must be in bounds"
        if self.grid[row][col].is_flagged == flag_val:
            return
        self.grid.grid[row][col].flag(flag_val)
        if flag_val:
            self.num_flags+=1
        else:
            self.num_flags-=1
        return
