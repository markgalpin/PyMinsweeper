""" 
This defines the engine grid -- for calculation we will probably add some extra cached information,
but for now this covers the grid only as is for any implementation.
"""
__author__ = 'Mark Galpin'
__version__ = '0.1'

from collections import namedtuple

DEFAULT_GRID_COLS=17
DEFAULT_GRID_ROWS=24
DEFAULT_NUM_MINES=85

RevealedValue = namedtuple('RevealedValue', ['is_mined','value'])
FullValue = namedtuple('FullValue', ['is_revealed', 'is_flagged', 'value'])

class Cell:
    is_revealed:        bool = False
    is_flagged:         bool = False
    is_mined:           bool = False
    _value:             int  = None
    surrounding_cells:  int  = None

    def flag(self, flag_val: bool = True) -> None:
        """Flags a cell.  Also has the ability to unflag by passing False"""
        assert self._is_initialized(), "The cell is not initialized"
        self.is_flagged = flag_val
        return

    def full_value(self) -> FullValue[bool, bool, int]:
            """ Returns the value of a cell as a tuple is_flagged, is_revealed, and an int (or None if its not revealed) """
            return (self.is_flagged, self.is_revealed, self._value)
        
    def revealed_value(self) -> int:
            """ Returns the int value of a revealed cell. This function has an assertion that the cell is, in fact, revealed"""
            result=self.full_value()
            assert not result.is_revealed and not result.is_flagged
            return result.value

    def reveal(self) -> RevealedValue[bool, int]:
        """Reveals a single cell
            returns tuple[bool,int]: a tuple containing whether the cell is mined, and the value
            returns None if the cell is flagged, as it does nothing in that case.
        """
        assert self._is_initialized(), "The cell is not initialized"
        if self.is_flagged: 
            return None   #Do nothing if the cell is flagged.  I am not asserting this to deal with human players mis-clicking.
        else:
            self.is_revealed = True
            return self.is_mined, self._value

    def __init__(self, surrounds: int = 8) -> None:
        self.surrounding_cells = surrounds #I haven't decided whether I will use this or not.
        return
    
    def _is_initialized(self) -> bool:
        if self.is_mined == False and self._value == None:
            return False
        else:
            return True
    
    def _set_mined(self) -> None:
        self.is_mined = True
        return
    
    def _set_value(self, value: int) -> None:
        assert self._value != None, "Can only set Cell.value once"
        assert value >= 0 and value < self.surrounding_cells, "Cell.value must be between 0 and the number of surrounding cells"
        self._value = value
        return

    def _set_as_edge(self) -> None:
        self.surrounding_cells=5
        return
        
    def _set_as_corner(self) -> None:
        self.surrounding_cells=3
        return

class Grid:
    grid: list[list[Cell]] = []
    num_rows:       int = 0
    num_cols:       int = 0
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
         self._populate_mines(mines)
         self._calculate_cell_values()
         return

    def _create_cells(self) -> None:
        self.grid = [[Cell()] * self.num_cols] * self.num_rows
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
        return
    
    def _populate_mines(self, mines: int):
         #There should probably be a rule to prevent mines from fully surrounding a square (e.g. generating an 8)
         # or even a full-up block of 3x3 square mines.  But for now, I am going to not worry about it.
         # NOTE: It could be interesting to see how it affects the win rate to implement a block limit rule.  Something to think about later.
         raise NotImplementedError()
    
    def _calculate_cell_values(self):
         raise NotImplemented

def test(rows: int, columns: int, mines:int) -> Grid:
    MyGrid = Grid(rows, columns, mines)
    return

test(DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS, DEFAULT_NUM_MINES)