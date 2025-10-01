""" 
This is the tests for play_grid
"""

__author__ = 'Mark Galpin'
__version__ = '0.1'
import pytest
import play_grid
from play_grid import Grid



num_cols = play_grid.DEFAULT_GRID_COLS

num_rows = play_grid.DEFAULT_GRID_ROWS

num_mines = play_grid.DEFAULT_NUM_MINES

mygrid = Grid(num_rows, num_cols, num_mines)

def test_cell_separation():
    assert mygrid.grid[0][0] is not mygrid.grid[0][1]
    assert mygrid.grid[0][0] is not mygrid.grid[1][0]

def test_size():
    assert mygrid.num_cols == num_cols
    assert mygrid.num_rows == num_rows
    assert mygrid.total_cells == (num_rows * num_cols)

def test_surrounds():
    """Test surrounds.  Should be 3 in the corners, 5 on the edges, and otherwise 8
    """
    for row_index, row in enumerate(mygrid.grid):
        assert row_index < num_rows
        for column_index, cell in enumerate(row):
            assert column_index < num_cols
            if row_index == 0 or row_index == (num_rows - 1):
                if column_index == 0 or column_index == (num_cols - 1): # test the corners and top/bottom edges
                    assert cell.surrounding_cells == 3, "Row: "+row_index.__str__()+" Column: "+column_index.__str__()
                else:
                    assert cell.surrounding_cells == 5, "Row: "+row_index.__str__()+" Column: "+column_index.__str__()
            else:
                if column_index == 0 or column_index == (num_cols - 1): # test the left/right edges:
                    assert cell.surrounding_cells == 5, "Row: "+row_index.__str__()+" Column: "+column_index.__str__()
                else: #test everything else
                    assert cell.surrounding_cells == 8, "Row: "+row_index.__str__()+" Column: "+column_index.__str__()
    return

def test_mines():
    """Tests that the number of mines is correct"""
    assert mygrid.num_mines==num_mines
    count = 0
    for row in mygrid.grid:
        for cell in row:
            if cell.is_mined: count+=1
    assert count == num_mines

def test_unrevealed():
    """Tests that all squares in the initial set are unrevealed"""
    count = 0
    for row in mygrid.grid:
        for cell in row:
            if cell.is_revealed: count+=1
    assert count == 0

def test_unflagged():
    """Tests that all squares in the initial set are unflagged"""
    count = 0
    for row in mygrid.grid:
        for cell in row:
            if cell.is_flagged: count+=1
    assert count == 0

def test_values_set():
    """Tests that all squares have a configured value"""
    for row in mygrid.grid:
        for cell in row:
            if not cell.is_mined:
                assert cell._value is not None #pylint: disable=protected-access
