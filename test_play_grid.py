""" 
This is the tests for play_grid
"""

__author__ = 'Mark Galpin'
__version__ = '0.1'
#import pytest
from play_grid import Grid

NUM_COLS = 5
NUM_ROWS = 5
NUM_MINES = 10

mygrid = Grid(NUM_ROWS, NUM_COLS, NUM_MINES)

def test_cell_separation():
    """Test the cells aren't all pointers to the same one."""
    assert mygrid.grid[0][0] is not mygrid.grid[0][1]
    assert mygrid.grid[0][0] is not mygrid.grid[1][0]
    assert mygrid[0][2] is mygrid.grid[0][2]

def test_size():
    """Test the grid is the expected size"""
    assert mygrid.num_cols == NUM_COLS
    assert mygrid.num_rows == NUM_ROWS
    assert mygrid.total_cells == (NUM_ROWS * NUM_COLS)

def test_cell_indicies():
    """Test that cell indices are configured"""
    for row_index, row in enumerate(mygrid.grid):
        assert row_index < NUM_ROWS
        for column_index, cell in enumerate(row):
            assert column_index < NUM_COLS
            assert cell.row_index == row_index
            assert cell.col_index == column_index

def test_surrounds():
    """Test surrounds.  Should be 3 in the corners, 5 on the edges, and otherwise 8
    """
    for row_index, row in enumerate(mygrid.grid):
        for column_index, cell in enumerate(row):
            if row_index == 0 or row_index == (NUM_ROWS - 1): # test corners and top/bottom edges
                if column_index == 0 or column_index == (NUM_COLS - 1):
                    assert cell.surrounding_cells == 3, \
                        "Row: "+str(row_index)+" Column: "+str(column_index)
                else:
                    assert cell.surrounding_cells == 5, \
                        "Row: "+str(row_index)+" Column: "+str(column_index)
            else:
                if column_index == 0 or column_index == (NUM_COLS - 1): # test the left/right edges:
                    assert cell.surrounding_cells == 5, \
                        "Row: "+str(row_index)+" Column: "+str(column_index)
                else: #test everything else
                    assert cell.surrounding_cells == 8, \
                        "Row: "+str(row_index)+" Column: "+str(column_index)
    return

def test_mines():
    """Tests that the number of mines is correct"""
    assert mygrid.num_mines==NUM_MINES
    count = 0
    for row in mygrid.grid:
        for cell in row:
            if cell._is_mined: #pylint: disable=protected-access
                count+=1
    assert count == NUM_MINES

def test_unrevealed():
    """Tests that all squares in the initial set are unrevealed"""
    count = 0
    for row in mygrid.grid:
        for cell in row:
            if cell.is_revealed:
                count+=1
    assert count == 0

def test_unflagged():
    """Tests that all squares in the initial set are unflagged"""
    count = 0
    for row in mygrid.grid:
        for cell in row:
            if cell.is_flagged:
                count+=1
    assert count == 0

def test_values_set():
    """Tests that all squares have a configured value"""
    for row in mygrid.grid:
        for cell in row:
            if not cell._is_mined: #pylint: disable=protected-access
                assert cell._value is not None #pylint: disable=protected-access
