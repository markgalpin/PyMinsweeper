""" 
This defines the engine grid -- for calculation we will probably add some extra cached information,
but for now this covers the grid only as is for any implementation.
"""
__author__ = 'Mark Galpin'
__version__ = '0.1'

from typing import NamedTuple
import random

class RevealedValue(NamedTuple):
    """NamedTuple for what happens when you reveal a square"""
    is_mined: bool
    value: int

class VisibleValue(NamedTuple):
    """NamedTuple for the value of a square"""
    is_flagged: bool
    is_revealed: bool
    value: int

class Cell:
    """A class for a single cell in the minesweeper play grid"""
    is_revealed:        bool = False
    is_flagged:         bool = False
    is_mined:           bool = False
    _value:             int  = None
    surrounding_cells:  int  = None
    row_index:          int  = None
    col_index:          int  = None

    def flag(self, flag_val: bool = True) -> None:
        """Flags a cell.  Also has the ability to unflag by passing False"""
        assert self._is_initialized(), "The cell is not initialized"
        self.is_flagged = flag_val

    def visible_value(self) -> VisibleValue:
        """ Returns the value of a cell as a tuple is_flagged, is_revealed, 
        and an int (or None if its not revealed) 
        """
        return VisibleValue(self.is_flagged, self.is_revealed, self._value)

    def revealed_value(self) -> int:
        """ Returns the int value of a revealed cell. 
        This function has an assertion that the cell is, in fact, revealed"""
        result=self.visible_value()
        assert result.is_revealed
        assert not result.is_flagged
        return result.value

    def reveal(self) -> RevealedValue:
        """Reveals a single cell
            returns tuple[bool,int]: a tuple containing whether the cell is mined, and the value
            returns None if the cell is flagged, as it does nothing in that case.
        """
        assert self._is_initialized(), "The cell is not initialized"
        if self.is_flagged:
            return None   #Do nothing if the cell is flagged.  I am not asserting this yet
        else:
            self.is_revealed = True
            return RevealedValue(self.is_mined, self._value)

    def __init__(self, surrounds: int = 8) -> None:
        self.surrounding_cells = surrounds #I haven't decided whether I will use this or not.
        return

    def _is_initialized(self) -> bool:
        if not self.is_mined and self._value is None:
            return False
        else:
            return True

    def _set_mined(self) -> None:
        self.is_mined = True
        return

    def _set_value(self, value: int) -> None:
        assert self._value is None, "Can only set Cell.value once"
        assert value >= 0 and value <= self.surrounding_cells, "Cell.value must be between 0 and \
            the number of surrounding cells"
        self._value = value
        return

    def _set_as_edge(self) -> None:
        self.surrounding_cells=5
        return

    def _set_as_corner(self) -> None:
        self.surrounding_cells=3
        return

class Grid:
    """This is the actual class for the base grid in play
    NOTE: I should add syntactic sugar for direct access to Grid later if it seems useful"""
    grid: list[list[Cell]] = []
    num_rows:       int = 0
    num_cols:       int = 0
    num_mines:      int = 0
    total_cells:    int = 0

    def __init__(self, rows: int, columns: int, mines: int):
        assert rows>3, "Must be at least a 3x3 grid, row doesn't work"
        assert columns>3, "Must be at least a 3x3 grid, column doesn't work"
        assert (mines > 0), "Must have at least 1 mine"
        self.num_rows=rows
        self.num_cols=columns
        self.total_cells=rows * columns
        assert (mines<self.total_cells), "mines must be less than the total number of cells"
        self._create_cells()
        self._set_indices()
        self._populate_mines(mines)
        self._calculate_cell_values()
        return

    def _create_cells(self) -> None:
        #pylint: disable=protected-access
        #allowing Grid protected access to Cell is fine.
        self.grid = [[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for cell in self.grid[0]: # Top Edge
            cell._set_as_edge()
        for cell in self.grid[self.num_rows-1]: #bottom edge
            cell._set_as_edge()
        for row in self.grid:
            row[0]._set_as_edge() #left edge
            row[self.num_cols-1]._set_as_edge() #right edge
        #now the four corners:
        self.grid[0][0]._set_as_corner()
        self.grid[0][self.num_cols-1]._set_as_corner()
        self.grid[self.num_rows-1][0]._set_as_corner()
        self.grid[self.num_rows-1][self.num_cols-1]._set_as_corner()
        #pylint: enable=protected-access
        return

    def _set_indices(self) -> None:
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                cell.row_index=row_index
                cell.col_index=col_index

    def _populate_mines(self, mines: int):
        #There should probably be a rule to prevent mines from fully surrounding a square
        # (e.g. generating an 8) or even a full-up block of 3x3 square mines.
        # But for now, I am going to not worry about it.
        # NOTE: It could be how a block limit rule it affects the win rate.
        while self.num_mines < mines:
            row_i=random.randint(0, self.num_rows-1)
            col_i=random.randint(0, self.num_cols-1)
            if not self.grid[row_i][col_i].is_mined:
                self.grid[row_i][col_i]._set_mined() #pylint: disable=protected-access
                self.num_mines+=1
        return NotImplementedError()

    def collect_surrounds(self, row: int, col: int) -> list[Cell]:
        """This function returns all the surrounding cells"""
        assert row >= 0 and row < self.num_rows, "Row must be in bounds"
        assert col >= 0 and col < self.num_cols, "Column must be in bounds"
        result: list[Cell]=[]
        if row != 0:
            if col != 0:
                result.append(self.grid[row-1][col-1]) #top left
            result.append(self.grid[row-1][col]) #top middle
            if col != (self.num_cols-1):
                result.append(self.grid[row-1][col+1]) #top right
        if col!=0:
            result.append(self.grid[row][col-1]) #middle left
        #skip self
        if col!=(self.num_cols-1):
            result.append(self.grid[row][col+1]) #middle right
        if row!=(self.num_rows-1):
            if col != 0:
                result.append(self.grid[row+1][col-1]) #bottom left
            result.append(self.grid[row+1][col]) #bottom middle
            if col != (self.num_cols-1):
                result.append(self.grid[row+1][col+1]) #bottom right
        return result

    def _calculate_cell_values(self) -> None:
        for row_index, row in enumerate(self.grid):
            for column_index, cell in enumerate(row):
                surrounds=self.collect_surrounds(row_index, column_index)
                count=0
                for s_cell in surrounds:
                    if s_cell.is_mined:
                        count+=1
                cell._set_value(count) #pylint: disable=protected-access
        return

    def __getitem__(self, key: int):
        assert key < self.num_rows, "Out of bounds row"
        return self.grid[key]

    def __iter__(self):
        return self.grid.__iter__()

    def serialize_playable(self) -> list[str]:
        """Outputs a character matrix of the "play screen" in ASCII"""
        result=[]
        for row in self.grid:
            outstr=""
            for cell in row:
                if cell.is_flagged:
                    outstr+="F"
                elif not cell.is_revealed:
                    outstr+="="
                else:
                    if cell.is_mined:
                        outstr+="@"
                    else:
                        value=cell.revealed_value()
                        if value == 0:
                            outstr+="."
                        else:
                            outstr+=str(value)
            result.append(outstr)
        return result

    def _serialize_reveal_all(self) -> list[str]:
        """Shows all squares"""
        result=[]
        for row in self.grid:
            outstr=""
            for cell in row:
                if cell.is_flagged:
                    if cell.is_mined:
                        outstr+="F"
                    else:
                        outstr+="X"
                else:
                    if cell.is_mined:
                        if cell.is_revealed:
                            outstr+="@"
                        else:
                            outstr+="*"
                    elif cell._value == 0: #pylint: disable=protected-access
                        outstr+="."
                    else:
                        outstr+=str(cell._value) #pylint: disable=protected-access
            result.append(outstr)
        return result
