""" 
This defines the minesweeper game engine
"""
__author__ = 'Mark Galpin'
__version__ = '0.1'

from play_grid import Grid

DEFAULT_GRID_COLS=17
DEFAULT_GRID_ROWS=24
DEFAULT_NUM_MINES=85

class Engine:
    """Functions for modifying the grid while playing"""
    grid: Grid = None
    num_flags: int = 0
    game_is_over: bool = False
    game_is_won: bool = False
    ascii_game_board: list[str] = None
    def __init__(self, num_rows, num_cols, num_mines):
        self.grid=Grid(num_rows, num_cols, num_mines)
        self.ascii_game_board=self.grid.serialize_playable()
        return

    def mines_remaining(self) -> int:
        """Gives the number of mines remaining"""
        assert self.grid.num_mines!=0
        assert self.num_flags <= self.grid.num_mines, "Flags: "+str(self.num_flags)+ \
            " Mines: "+str(self.grid.num_mines)+"\n"+str(self)
        return self.grid.num_mines-self.num_flags

    def update_board_state(self) -> list[str]:
        """Updates the ascii board and performs end-game checks"""
        assert not self.game_is_over
        self.ascii_game_board=self.grid.serialize_playable()
        if self.mines_remaining() == 0:
            for row in self.grid:
                for cell in row:
                    if not cell.is_flagged and not cell.is_revealed:
                        if self.reveal_cell(cell.row_index, cell.col_index):
                            return self.ascii_game_board
            if not self.game_is_over:
                self.game_is_won=True
                self.game_is_over=True
                self.ascii_game_board=self.grid.serialize_playable()
        return self.ascii_game_board

    def reveal_cell(self, row: int, col: int) -> bool:
        """reveals the cell, plus other cells if its empty.  Returns true if boom!"""
        assert row >= 0 and row < self.grid.num_rows, "Row must be in bounds"
        assert col >= 0 and col < self.grid.num_cols, "Column must be in bounds"
        if self.grid[row][col].is_revealed:
            return False
        if self.grid[row][col].is_flagged:
            return False
        result=self.grid[row][col].reveal()
        assert result is not None
        if result.is_mined:
            self.went_boom()
            return True
        if result.value==0:
            surrounds=self.grid.collect_surrounds(row, col)
            for cell in surrounds:
                inner_result=self.reveal_cell(cell.row_index, cell.col_index)
                assert not inner_result, str(self)
        if not self.game_is_over:
            self.update_board_state()
        return False

    def flag_cell(self, row: int, col: int, flag_val: bool = True) -> None:
        """Flags a cell at the specified coordinate.  pass False to unflag"""
        assert row >= 0 and row < self.grid.num_rows, "Row must be in bounds"
        assert col >= 0 and col < self.grid.num_cols, "Column must be in bounds"
        if self.grid[row][col].is_flagged == flag_val:
            return
        self.grid[row][col].flag(flag_val)
        if flag_val:
            self.num_flags+=1
        else:
            self.num_flags-=1
        self.update_board_state()
        return

    def went_boom(self) -> list[str]:
        """Handles what happens when you go boom!"""
        self.game_is_over=True
        self.ascii_game_board=self.grid._serialize_reveal_all() #pylint: disable=protected-access
        return self.ascii_game_board

    def __str__(self) -> str:
        return "\n".join(self.ascii_game_board)
